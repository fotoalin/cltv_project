from datetime import datetime

import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import UploadFileForm
from .models import CLTVResult, CustomerData


def calculate_cltv(data):
    try:
        data["start_date"] = pd.to_datetime(data["start_date"])
        data["end_date"] = pd.to_datetime(data["end_date"])

        data["lifespan"] = (data["end_date"] - data["start_date"]).dt.days / 365.25

        avg_customer_lifespan = data["lifespan"].mean().item()
        total_revenue = data["revenue"].sum().item()
        num_purchases = data["num_purchases"].sum().item()
        num_customers = int(data.shape[0])

        apv = total_revenue / num_purchases
        apfr = num_purchases / num_customers
        cv = apv * apfr
        cltv = cv * avg_customer_lifespan

        return {
            "cltv": float(cltv),
            "avg_customer_lifespan": float(avg_customer_lifespan),
            "total_revenue": float(total_revenue),
            "num_purchases": int(num_purchases),
            "num_customers": int(num_customers),
            "apv": float(apv),
            "apfr": float(apfr),
            "cv": float(cv),
            "individual_lifespans": [float(lifespan) for lifespan in data["lifespan"]],
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
                required_columns = {
                    "customer_id",
                    "start_date",
                    "end_date",
                    "revenue",
                    "num_purchases",
                }
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
