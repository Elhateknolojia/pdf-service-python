from flask import Flask, request, Response
from weasyprint import HTML

app = Flask(__name__)

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        html_content = request.data.decode("utf-8")
        pdf = HTML(string=html_content).write_pdf()

        return Response(
            pdf,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=Acres_of_Mercy_Prospectus.pdf"
            }
        )
    except Exception as e:
        print("PDF generation failed:", e)
        return Response("Failed to generate PDF", status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
