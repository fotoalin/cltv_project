from datetime import datetime

import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import UploadFileForm
from .models import CLTVResult, CustomerData


def calculate_cltv(data):
    try:
        data["order_date"] = pd.to_datetime(data["order_date"])

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
        }
    except Exception as e:
        raise ValueError("Error in calculating CLTV: " + str(e))


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
    except CLTVResult.DoesNotExist:
        messages.error(request, "Result not found.")
        return redirect("upload_file")
    return render(
        request,
        "cltv_app/result.html",
        {"cltv_result": cltv_result, "detailed_data": detailed_data},
    )
