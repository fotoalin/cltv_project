from datetime import datetime

# def generate_recommendations(detailed_data):
#     # detailed_data keys:
#     # cltv
#     # avg_customer_lifespan
#     # total_revenue
#     # num_purchases
#     # num_customers
#     # apv
#     # apfr
#     # cv
#     # individual_lifespans
#     # overall_start_date
#     # overall_end_date
#     # customer_data
#     # cac
#     # avg_num_purchases
#     # customer_segments
#     # customer_recommendations
#     # revenue_by_year_segment
#     recommendations = []

#     # Convert date strings to datetime objects
#     overall_start_date = datetime.fromisoformat(detailed_data['overall_start_date'])
#     overall_end_date = datetime.fromisoformat(detailed_data['overall_end_date'])

#     # Short Customer Lifespan
#     if detailed_data['avg_customer_lifespan'] < 0.5:
#         recommendations.append({
#             'title': 'Short Customer Lifespan',
#             'description': f'The average customer lifespan of {detailed_data["avg_customer_lifespan"]:.2f} years (around {round(365 * detailed_data["avg_customer_lifespan"])} days) suggests a high customer churn rate. Investigate why customers do not return after their initial purchases. Consider strategies to improve customer retention, such as loyalty programs or follow-up marketing campaigns.'
#         })
#     elif detailed_data['avg_customer_lifespan'] < 1:
#         recommendations.append({
#             'title': 'Very Short Customer Lifespan',
#             'description': 'The average customer lifespan is very short. Consider implementing retention strategies such as loyalty programs or personalized follow-ups.'
#         })
#     elif detailed_data['avg_customer_lifespan'] < 3:
#         recommendations.append({
#             'title': 'High Customer Lifespan',
#             'description': 'The average customer lifespan is high. Focus on maintaining customer engagement and satisfaction.'
#         })
#     elif detailed_data['avg_customer_lifespan'] < 5:
#         recommendations.append({
#             'title': 'Very High Customer Lifespan',
#             'description': 'The average customer lifespan is very high. Keep up the good work!'
#         })

#     # Average Purchase Value
#     if detailed_data['apv'] < 50:
#         recommendations.append({
#             'title': 'Low Average Purchase Value',
#             'description': 'The average purchase value is relatively low. Consider upselling or bundling products to increase the average order value.'
#         })

#     # Average Purchase Frequency Rate
#     if detailed_data['apfr'] < 2:
#         recommendations.append({
#             'title': 'Low Purchase Frequency Rate',
#             'description': 'The average purchase frequency rate is low. Encourage repeat purchases through email campaigns and reminders.'
#         })

#     # Customer Value
#     if detailed_data['cv'] < 100:
#         recommendations.append({
#             'title': 'Low Customer Value',
#             'description': 'The customer value is low. Focus on increasing both the purchase frequency and average purchase value.'
#         })

#     # Customer Acquisition Cost vs Customer Lifetime Value
#     if detailed_data['cac'] > detailed_data['cltv']:
#         recommendations.append({
#             'title': 'High Customer Acquisition Cost',
#             'description': 'The customer acquisition cost is higher than the customer lifetime value. Optimize your marketing spend to acquire customers more cost-effectively.'
#         })

#     # Total Revenue
#     if detailed_data['total_revenue'] < 1000000:
#         recommendations.append({
#             'title': 'Low Total Revenue',
#             'description': 'Total revenue is relatively low. Focus on increasing customer acquisition and retention to drive revenue growth.'
#         })
#     if 1000000 <= detailed_data['total_revenue'] < 5000000:
#         recommendations.append({
#             'title': 'High Total Revenue',
#             'description': 'Total revenue is high. Maintain the momentum by investing in customer retention and acquisition strategies.'
#         })
#     if detailed_data['total_revenue'] >= 5000000:
#         recommendations.append({
#             'title': 'Very High Total Revenue',
#             'description': 'Total revenue is very high. Keep up the good work!'
#         })

#     # Further analysis based on dynamic data
#     if detailed_data['num_purchases'] > 1000 and detailed_data['avg_customer_lifespan'] < 0.5:
#         recommendations.append({
#             'title': 'High Transaction Volume but Low Retention',
#             'description': 'The high number of purchases and revenue indicates good market activity, but the retention is poor. Focus on enhancing the customer experience to encourage repeat purchases.'
#         })

#     if detailed_data['cltv'] < 100 and detailed_data['cac'] < 50:
#         recommendations.append({
#             'title': 'Reevaluate Customer Acquisition Strategies',
#             'description': 'Given the low CLTV, it’s crucial to optimize customer acquisition costs. However, the very low CAC suggests that the company is not spending much on acquiring customers, which might be fine but should be validated.'
#         })

#     if detailed_data['apfr'] >= 2 and detailed_data['avg_num_purchases'] >= 3:
#         recommendations.append({
#             'title': 'Improve Engagement',
#             'description': 'Since the APFR and Average Number of Purchases suggest customers do engage a few times, work on converting these few engagements into longer-term relationships. Implement engagement strategies such as personalized offers, excellent customer service, and regular communication.'
#         })

#     if (overall_end_date - overall_start_date).days / 30 < 12:
#         recommendations.append({
#             'title': 'Data Quality and Duration',
#             'description': 'The short period of data might skew the lifespan calculation. Ensure that the dataset is comprehensive and covers a more extended period for more accurate insights.'
#         })

#     if 'customer_segments' in detailed_data and detailed_data['customer_segments']:
#         recommendations.append({
#             'title': 'Further Analysis',
#             'description': 'Conduct further segmentation to identify patterns within customer behavior. Perhaps certain customer segments (e.g., based on demographics or purchase behavior) exhibit longer lifespans and higher values.'
#         })

#     # Next Steps
#     recommendations.append({
#         'title': 'Next Steps',
#         'description': '<ul><li>Extend Data Collection Period: Collect and analyze data over a more extended period to get a more accurate picture of customer lifespan and behavior.</li><li>Customer Feedback: Gather feedback from customers to understand why they might not be returning and address those issues.</li><li>Retention Programs: Implement programs focused on retaining customers beyond their initial purchases.</li></ul>'
#     })

#     return recommendations





def generate_recommendations(detailed_data):
    # detailed_data keys:
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
    recommendations = []

    # Convert date strings to datetime objects
    overall_start_date = datetime.fromisoformat(detailed_data['overall_start_date'])
    overall_end_date = datetime.fromisoformat(detailed_data['overall_end_date'])

    # Short Customer Lifespan
    if detailed_data['avg_customer_lifespan'] < 0.5:
        recommendations.append({
            'title': 'Short Customer Lifespan',
            'description': f'The average customer lifespan of <strong>{detailed_data["avg_customer_lifespan"]:.2f}</strong> years (<strong>around {round(365 * detailed_data["avg_customer_lifespan"])} days</strong>) suggests a high customer churn rate. Investigate why customers do not return after their initial purchases. Consider strategies to improve customer retention, such as loyalty programs or follow-up marketing campaigns.'
        })
    elif detailed_data['avg_customer_lifespan'] < 1:
        recommendations.append({
            'title': 'Very Short Customer Lifespan',
            'description': 'The average customer lifespan is very short. Consider implementing retention strategies such as loyalty programs or personalized follow-ups.'
        })
    elif detailed_data['avg_customer_lifespan'] < 3:
        recommendations.append({
            'title': 'High Customer Lifespan',
            'description': 'The average customer lifespan is high. Focus on maintaining customer engagement and satisfaction.'
        })
    elif detailed_data['avg_customer_lifespan'] < 5:
        recommendations.append({
            'title': 'Very High Customer Lifespan',
            'description': 'The average customer lifespan is very high. Keep up the good work!'
        })

    # Average Purchase Value
    if detailed_data['apv'] < 50:
        recommendations.append({
            'title': 'Low Average Purchase Value',
            'description': 'The average purchase value is relatively low. Consider upselling or bundling products to increase the average order value.'
        })

    # Average Purchase Frequency Rate
    if detailed_data['apfr'] < 2:
        recommendations.append({
            'title': 'Low Purchase Frequency Rate',
            'description': 'The average purchase frequency rate is low. Encourage repeat purchases through email campaigns and reminders.'
        })

    # Customer Value
    if detailed_data['cv'] < 100:
        recommendations.append({
            'title': 'Low Customer Value',
            'description': 'The customer value is low. Focus on increasing both the purchase frequency and average purchase value.'
        })

    # Customer Acquisition Cost vs Customer Lifetime Value
    if detailed_data['cac'] >= 0.3 * detailed_data['cltv']:
        recommendations.append({
            'title': 'Customer Acquisition Cost Management',
            'description': 'The customer acquisition cost is 30% or more of the customer lifetime value. Ensure that the marketing and sales strategies are optimized to maintain this ratio while still acquiring valuable customers.'
        })
    else:
        recommendations.append({
            'title': 'Efficient Customer Acquisition Cost',
            'description': 'The customer acquisition cost is less than 30% of the customer lifetime value. This indicates an efficient acquisition strategy. Maintain this efficiency while scaling your customer base.'
        })

    # Total Revenue
    if detailed_data['total_revenue'] < 1000000:
        recommendations.append({
            'title': 'Low Total Revenue',
            'description': 'Total revenue is relatively low. Focus on increasing customer acquisition and retention to drive revenue growth.'
        })
    elif 1000000 <= detailed_data['total_revenue'] < 5000000:
        recommendations.append({
            'title': 'High Total Revenue',
            'description': 'Total revenue is high. Maintain the momentum by investing in customer retention and acquisition strategies.'
        })
    elif detailed_data['total_revenue'] >= 5000000:
        recommendations.append({
            'title': 'Very High Total Revenue',
            'description': 'Total revenue is very high. Keep up the good work!'
        })

    # Further analysis based on dynamic data
    if detailed_data['num_purchases'] > 1000 and detailed_data['avg_customer_lifespan'] < 0.5:
        recommendations.append({
            'title': 'High Transaction Volume but Low Retention',
            'description': 'The high number of purchases and revenue indicates good market activity, but the retention is poor. Focus on enhancing the customer experience to encourage repeat purchases.'
        })

    if detailed_data['cltv'] < 100 and detailed_data['cac'] < 50:
        recommendations.append({
            'title': 'Reevaluate Customer Acquisition Strategies',
            'description': 'Given the low CLTV, it’s crucial to optimize customer acquisition costs. However, the very low CAC suggests that the company is not spending much on acquiring customers, which might be fine but should be validated.'
        })

    if detailed_data['apfr'] >= 2 and detailed_data['avg_num_purchases'] >= 3:
        recommendations.append({
            'title': 'Improve Engagement',
            'description': 'Since the APFR and Average Number of Purchases suggest customers do engage a few times, work on converting these few engagements into longer-term relationships. Implement engagement strategies such as personalized offers, excellent customer service, and regular communication.'
        })

    if (overall_end_date - overall_start_date).days / 30 < 12:
        recommendations.append({
            'title': 'Data Quality and Duration',
            'description': 'The short period of data might skew the lifespan calculation. Ensure that the dataset is comprehensive and covers a more extended period for more accurate insights.'
        })

    if 'customer_segments' in detailed_data and detailed_data['customer_segments']:
        recommendations.append({
            'title': 'Further Analysis',
            'description': 'Conduct further segmentation to identify patterns within customer behavior. Perhaps certain customer segments (e.g., based on demographics or purchase behavior) exhibit longer lifespans and higher values.'
        })

    # Business Administration
    if detailed_data['cac'] > 50:  # Example threshold for high CAC
        recommendations.append({
            'title': 'Operational Efficiency',
            'description': f'Based on the data, consider streamlining operations to reduce the Customer Acquisition Cost (CAC) of <strong>£{detailed_data["cac"]:,}</strong>. Implementing more efficient processes or leveraging automation can help achieve this.'
        })

    # Marketing
    if detailed_data['apfr'] >= 1:  # Example threshold for sufficient data on APFR
        recommendations.append({
            'title': 'Targeted Marketing Campaigns',
            'description': f'With an Average Purchase Frequency Rate (APFR) of <strong>{detailed_data["apfr"]:.2f}</strong>, personalized marketing campaigns can help increase engagement. Utilize customer data to tailor promotions and messages.'
        })

    # Finance
    if detailed_data['total_revenue'] > 500000:  # Example threshold for significant revenue
        recommendations.append({
            'title': 'Financial Planning',
            'description': f'The total revenue of <strong>£{detailed_data["total_revenue"]:,}</strong> indicates potential for further investment. Evaluate the ROI of current marketing strategies and consider reallocating budget to high-performing channels.'
        })

    # Data Science
    if 'customer_data' in detailed_data and len(detailed_data['customer_data']) > 100:  # Example threshold for sufficient data
        recommendations.append({
            'title': 'Predictive Analytics',
            'description': 'Implement predictive analytics to anticipate customer behavior and improve retention strategies. Use historical data to predict future trends and tailor customer experiences accordingly.'
        })

    # Computer Science
    if detailed_data['num_purchases'] > 1000:  # Example threshold for high volume of transactions
        recommendations.append({
            'title': 'System Scalability',
            'description': f'With over <strong>{detailed_data["num_purchases"]:,}</strong> purchases, ensure your system architecture can scale efficiently. Consider leveraging cloud infrastructure and optimizing code for better performance.'
        })

    # Next Steps
    recommendations.append({
        'title': 'Next Steps',
        'description': '<ul><li>Extend Data Collection Period: Collect and analyze data over a more extended period to get a more accurate picture of customer lifespan and behavior.</li><li>Customer Feedback: Gather feedback from customers to understand why they might not be returning and address those issues.</li><li>Retention Programs: Implement programs focused on retaining customers beyond their initial purchases.</li></ul>'
    })

    return recommendations
