from flask import Flask, render_template, request
from jobspy import scrape_jobs


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    jobs = []
    if request.method == "POST":
        job_title = request.form.get("job_title")
        location = request.form.get("location")
        
        # Run the JobSpy scrape
        jobs_df = scrape_jobs(
            site_name=["linkedin"],
            search_term=job_title,
            location=location,
            results_wanted=100,
            hours_old=72,
            country_indeed='USA'
        )
        jobs = jobs_df.to_dict(orient="records")

    return render_template("jobs.html", jobs=jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



