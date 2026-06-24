import os
import logging
from flask import Flask, request, Response
from playwright.sync_api import sync_playwright

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

app = Flask(__name__)

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        logging.info("📥 Request received at /generate-pdf")
        logging.info("Headers: %s", dict(request.headers))
        logging.info("Content-Type: %s", request.content_type)

        # Decode HTML body
        html_content = request.data.decode("utf-8")
        logging.info("HTML length: %d", len(html_content))
        logging.info("HTML preview: %s", html_content[:200])

        if not html_content.strip():
            logging.error("❌ Error: Empty HTML content received")
            return Response("No HTML content provided", status=400)

        # Launch Playwright
        logging.info("🖥️ Launching Chromium via Playwright...")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                args=["--no-sandbox", "--disable-setuid-sandbox"],
                headless=True
            )
            page = browser.new_page()

            # Set HTML content
            logging.info("📄 Setting page content...")
            page.set_content(html_content, wait_until="networkidle")

            # Generate PDF
            logging.info("🖨️ Generating PDF...")
            pdf = page.pdf(format="A4", print_background=True)
            logging.info("✅ PDF generated successfully, size: %d bytes", len(pdf))

            browser.close()

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
