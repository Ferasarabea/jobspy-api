from flask import Flask, render_template, request
from jobspy import scrape_jobs
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    jobs = []
    if request.method == "POST":
        job_title = request.form.get("job_title")
        location = request.form.get("location")

        try:
            # Run the JobSpy scrape
            jobs_df = scrape_jobs(
                site_name=["linkedin", "indeed"],  # fixed typo and removed unsupported site
                search_term=job_title,
                location=location,
                results_wanted=100,
                hours_old=72,  # 14 days only
                country_indeed='USA'
            )

            # Manual location filter
            if location:
                jobs_df = jobs_df[
                    jobs_df['location'].str.contains(location, case=False, na=False)
                ]

            jobs = jobs_df.fillna("").to_dict(orient="records")

        except Exception as e:
            print("Scraping error:", e)

    return render_template("jobs.html", jobs=jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




