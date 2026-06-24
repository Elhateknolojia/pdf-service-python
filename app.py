import os
from flask import Flask, request, Response
from weasyprint import HTML

app = Flask(__name__)

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    try:
        # Log raw request info
        print("📥 Received request to /generate-pdf")
        print("Headers:", dict(request.headers))
        print("Content-Type:", request.content_type)

        # Decode HTML body
        html_content = request.data.decode("utf-8")
        print("HTML length:", len(html_content))
        print("HTML preview:", html_content[:200])  # log first 200 chars

        if not html_content.strip():
            print("❌ Error: Empty HTML content received")
            return Response("No HTML content provided", status=400)

        # Generate PDF
        pdf = HTML(string=html_content).write_pdf()
        print("✅ PDF generated successfully, size:", len(pdf), "bytes")

        return Response(
            pdf,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=Acres_of_Mercy_Prospectus.pdf"
            }
        )
    except Exception as e:
        print("❌ PDF generation failed:", e)
        return Response("Failed to generate PDF", status=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns dynamic port
    print(f"🚀 Starting Flask server on port {port}")
    app.run(host="0.0.0.0", port=port)
