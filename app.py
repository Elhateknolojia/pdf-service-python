import os
import logging
from flask import Flask, request, Response
from weasyprint import HTML

app = Flask(__name__)

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        logging.info("📥 Request received at /generate-pdf")
        logging.info("Headers: %s", dict(request.headers))
        logging.info("Content-Type: %s", request.content_type)

        html_content = request.data.decode("utf-8")
        logging.info("HTML length: %d", len(html_content))
        logging.info("HTML preview: %s", html_content[:200])

        if not html_content.strip():
            logging.error("❌ Error: Empty HTML content received")
            return Response("No HTML content provided", status=400)

        pdf = HTML(string=html_content).write_pdf()
        logging.info("✅ PDF generated successfully, size: %d bytes", len(pdf))

        return Response(
            pdf,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=Acres_of_Mercy_Prospectus.pdf"
            }
        )
    except Exception as e:
        logging.exception("❌ PDF generation failed")
        return Response("Failed to generate PDF", status=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logging.info("🚀 Starting Flask server on port %d", port)
    app.run(host="0.0.0.0", port=port)
