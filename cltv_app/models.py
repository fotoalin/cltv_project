from django.db import models


class CustomerData(models.Model):
    upload = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class CLTVResult(models.Model):
    customer_data = models.OneToOneField(CustomerData, on_delete=models.CASCADE)
    cltv = models.DecimalField(max_digits=10, decimal_places=2)
    calculated_at = models.DateTimeField(auto_now_add=True)

    # -- Add additional fields here  --
    # cltv
    # avg_customer_lifespan
    # total_revenue
    # num_purchases
    # num_customers
    # apv
    # apfr
    # cv
    # individual_lifespans
    # overall_start_date
    # overall_end_date
    # customer_data
    # cac
    # avg_num_purchases
    # customer_segments
    # customer_recommendations
    # revenue_by_year_segment