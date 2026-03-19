import { Download } from "lucide-react";
import Button from "../ui/Button";

export default function ExportPDF() {
  const handleExport = async () => {
    const element = document.getElementById("itinerary-content");
    if (!element) return;

    const html2canvas = (await import("html2canvas")).default;
    const { jsPDF } = await import("jspdf");

    const canvas = await html2canvas(element, { scale: 2 });
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");
    const imgWidth = 210;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    let heightLeft = imgHeight;
    let position = 0;

    pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
    heightLeft -= 297;

    while (heightLeft > 0) {
      position = heightLeft - imgHeight;
      pdf.addPage();
      pdf.addImage(imgData, "PNG", 0, position, imgWidth, imgHeight);
      heightLeft -= 297;
    }

    pdf.save("fravel-itinerary.pdf");
  };

  return (
    <Button variant="secondary" size="sm" onClick={handleExport}>
      <Download size={14} />
      Export PDF
    </Button>
  );
}
