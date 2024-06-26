import matplotlib

matplotlib.use("Agg")
import base64
import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from reportlab.pdfgen import canvas

from .forms import UploadFileForm
from .models import CLTVResult, CustomerData


def calculate_cltv(data):
    try:
        data["order_date"] = pd.to_datetime(data["order_date"])
        data["year"] = data["order_date"].dt.year

        # Aggregate data per customer
        customer_data = (
            data.groupby("customer_id")
            .agg(
                start_date=("order_date", "min"),
                end_date=("order_date", "max"),
                revenue=("revenue", "sum"),
                num_purchases=("order_id", "count"),
            )
            .reset_index()
        )

        customer_data["lifespan"] = (
            customer_data["end_date"] - customer_data["start_date"]
        ).dt.days / 365.25

        avg_customer_lifespan = customer_data["lifespan"].mean().item()
        total_revenue = customer_data["revenue"].sum().item()
        num_purchases = customer_data["num_purchases"].sum().item()
        num_customers = int(customer_data.shape[0])

        apv = total_revenue / num_purchases
        apfr = num_purchases / num_customers
        cv = apv * apfr
        cltv = cv * avg_customer_lifespan

        overall_start_date = customer_data["start_date"].min().isoformat()
        overall_end_date = customer_data["end_date"].max().isoformat()

        customer_data["start_date"] = customer_data["start_date"].dt.date.astype(str)
        customer_data["end_date"] = customer_data["end_date"].dt.date.astype(str)

        # Calculate Customer Acquisition Cost (CAC) as 30% of CLTV
        cac = cltv * 0.30

        # Calculate Average Number of Purchases per Customer
        avg_num_purchases = num_purchases / num_customers

        # Define segments based on revenue
        bins = [4, 16, 75, 150, np.inf]
        labels = ["Low", "Medium", "High", "VIP"]
        customer_data["segment"] = pd.cut(
            customer_data["revenue"], bins=bins, labels=labels, right=False
        )

        # Merge segment information back to the main data
        data = data.merge(
            customer_data[["customer_id", "segment"]], on="customer_id", how="left"
        )

        # Generate recommendations
        def get_recommendations(segment):
            recommendations = {
                "Low": "Offer discounts or promotions to increase engagement.",
                "Medium": "Provide loyalty programs and personalized communication.",
                "High": "Enhance customer service and offer exclusive deals.",
                "VIP": "Consider personalized account management and premium services.",
            }
            return recommendations.get(segment, "No recommendation available.")

        customer_data["recommendation"] = customer_data["segment"].apply(
            get_recommendations
        )

        # Aggregate revenue by year and segment
        revenue_by_year_segment = (
            data.groupby(["year", "segment"])["revenue"].sum().unstack(fill_value=0)
        )

        return {
            "cltv": float(cltv),
            "avg_customer_lifespan": float(avg_customer_lifespan),
            "total_revenue": float(total_revenue),
            "num_purchases": int(num_purchases),
            "num_customers": int(num_customers),
            "apv": float(apv),
            "apfr": float(apfr),
            "cv": float(cv),
            "individual_lifespans": [
                float(lifespan) for lifespan in customer_data["lifespan"]
            ],
            "overall_start_date": overall_start_date,
            "overall_end_date": overall_end_date,
            "customer_data": customer_data.to_dict(orient="records"),
            "cac": float(cac),
            "avg_num_purchases": float(avg_num_purchases),
            "customer_segments": customer_data[["customer_id", "segment"]].to_dict(
                orient="records"
            ),
            "customer_recommendations": customer_data[
                ["customer_id", "recommendation"]
            ].to_dict(orient="records"),
            "revenue_by_year_segment": revenue_by_year_segment.to_dict(orient="index"),
        }
    except Exception as e:
        raise ValueError("Error in calculating CLTV: " + str(e))


def create_dashboard(revenue_by_year_segment):
    df = pd.DataFrame(revenue_by_year_segment).fillna(0)
    fig, ax = plt.subplots(figsize=(10, 6))

    df.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")

    ax.set_ylabel("Revenue (£)")
    ax.set_xlabel("Year")
    ax.set_title("Revenue by Year and Customer Segment")
    ax.legend(title="Customer Segment")

    # Annotate the bars with the value
    for container in ax.containers:
        ax.bar_label(container, fmt="£%.2f")

    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)  # Close the figure to free memory
    return plot_url


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            customer_data = form.save()
            file = request.FILES["upload"]
            try:
                data = pd.read_excel(file)
                # Validate data
                required_columns = {"order_id", "customer_id", "order_date", "revenue"}
                if not required_columns.issubset(data.columns):
                    messages.error(
                        request,
                        "Invalid file format. Please ensure the file has the required columns.",
                    )
                    return redirect("upload_file")

                cltv_result_data = calculate_cltv(data)
                cltv_result = CLTVResult.objects.create(
                    customer_data=customer_data, cltv=cltv_result_data["cltv"]
                )

                # Store the detailed result data in the session
                request.session["detailed_data"] = cltv_result_data

                return redirect("result", result_id=cltv_result.id)
            except Exception as e:
                messages.error(request, "Error processing file: " + str(e))
                return redirect("upload_file")
    else:
        form = UploadFileForm()
    return render(request, "cltv_app/upload.html", {"form": form})


def result(request, result_id):
    try:
        cltv_result = CLTVResult.objects.get(id=result_id)
        detailed_data = request.session.get("detailed_data")
        if not detailed_data:
            messages.error(request, "Detailed data not found in session.")
            return redirect("upload_file")

        plot_url = create_dashboard(detailed_data["revenue_by_year_segment"])
    except CLTVResult.DoesNotExist:
        messages.error(request, "Result not found.")
        return redirect("upload_file")
    return render(
        request,
        "cltv_app/result.html",
        {
            "cltv_result": cltv_result,
            "detailed_data": detailed_data,
            "plot_url": plot_url,
        },
    )


def generate_report(data):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="customer_insights.pdf"'
    p = canvas.Canvas(response)
    p.drawString(100, 750, "Customer Insights Report")
    p.drawString(100, 730, f"CLTV: £{data['cltv']:.2f}")
    p.drawString(
        100,
        710,
        f"Average Customer Lifespan: {data['avg_customer_lifespan']:.2f} years",
    )
    # Add more details as needed
    p.showPage()
    p.save()
    return response


def download_report(request, result_id):
    detailed_data = request.session.get("detailed_data")
    if not detailed_data:
        messages.error(request, "Detailed data not found in session.")
        return redirect("upload_file")
    return generate_report(detailed_data)
