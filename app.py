from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("results.csv")

df["seating_no"] = df["seating_no"].astype(str)

@app.route("/", methods=["GET", "POST"])
def index():
    student = None
    error = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if not query:
            error = "الرجاء إدخال رقم الجلوس أو الاسم."
        else:

            result = df[
                (df["seating_no"] == query) |
                (df["arabic_name"].str.contains(query, case=False, na=False))
            ]

            if result.empty:
                error = "❌ لا توجد نتيجة بهذا الرقم أو الاسم."
            else:

                student = result.iloc[0].to_dict()
                student["is_passed"] = "ناجح" in student["student_case_desc"]

    return render_template("index.html", student=student, error=error)

if __name__ == "__main__":
    app.run(debug=True)
