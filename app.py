from flask import Flask, render_template, request, jsonify
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

# ✅ Added API endpoint
@app.route("/api/scrape", methods=["POST"])
def scrape_api():
    data = request.json
    job_title = data.get("job_title")
    location = data.get("location")

    try:
        jobs_df = scrape_jobs(
            site_name=["linkedin", "indeed"],
            search_term=job_title,
            location=location,
            results_wanted=100,
            hours_old=72,
            country_indeed='USA'
        )

        if location:
            jobs_df = jobs_df[
                jobs_df['location'].str.contains(location, case=False, na=False)
            ]

        jobs = jobs_df.fillna("").to_dict(orient="records")
        return jsonify({"success": True, "jobs": jobs})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




