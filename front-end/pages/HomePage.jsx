"use client";
import Image from "next/image";
import React, { useState, useEffect } from "react";
import { FiUpload } from "react-icons/fi";

function HomePage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFileName, setSelectedFileName] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    setSelectedFileName(file ? file.name : "");
  };

  const handleSamplePDF = async () => {
    setLoading(true);
    try {
      // If sample.pdf is in your frontend public folder:
      const res = await fetch("/sample.pdf");
      if (!res.ok) throw new Error("Sample PDF not found");
      console.log(res);
      const blob = await res.blob();
      const file = new File([blob], "sample.pdf", { type: "application/pdf" });
      setSelectedFile(file);
      setSelectedFileName("sample.pdf");
    } catch (error) {
      console.error("Failed to load sample PDF:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Only upload if a file is selected
    if (!selectedFile) return;
    setLoading(true);
    const loadPDF = async () => {
      const formData = new FormData();
      formData.append("file", selectedFile);
      try {
        const res = await fetch("http://localhost:8000/", {
          method: "POST",
          body: formData,
        });
        if (!res.ok) {
          throw new Error("Failed to upload file");
        } else {
          window.location.href = "/results";
        }
      } catch (error) {
        console.error("Error uploading file:", error);
      } finally {
        setLoading(false);
      }
    };

    loadPDF();
  }, [selectedFile]);

  return (
    <div className="flex flex-col h-screen p-4">
      <div>
        <h1 className="text-3xl text-stone-500 font-bold m-7">PDFAtoZ</h1>
      </div>
      <div className="flex items-center border-2 border-dashed border-gray-400 rounded-lg p-2 w-[400px] ml-[570px] mt-[170px] m-8">
        <label className="cursor-pointer bg-black text-white px-4 py-2 border-2 border-gray-500 rounded shadow hover:bg-gray-800 transition flex items-center gap-2">
          <FiUpload className="text-xl" />
          <input type="file" className="hidden" onChange={handleFileChange} />
        </label>
        <span className="ml-2 text-gray-700">
          {selectedFileName || "No file selected."}
        </span>
      </div>
      <button
        disabled={!selectedFile || loading}
        className=" ml-auto bg-blue-500 text-white px-4 py-2 rounded shadow hover:bg-blue-600 transition"
        onClick={() => {
          window.location.href = "/results";
        }}
      >
        View results
      </button>
      {selectedFile && (
        <div className="flex items-center justify-center mt-4">
          <div className="bg-gray-100 p-4 rounded shadow">
            <p>
              <strong>File Name:</strong> {selectedFile.name}
            </p>
            <p>
              <strong>File Size:</strong> {selectedFile.size} bytes
            </p>
            <p>
              <strong>File Type:</strong> {selectedFile.type}
            </p>
          </div>
        </div>
      )}
      <div className="top-0 left-0 right-0 bottom-0 flex items-center justify-center">
        <Image src="/arrow.png" alt="Logo" width={100} height={100} />
        <button
          className="bg-green-500 text-white px-4 py-2 rounded shadow hover:bg-green-600 transition mt-4"
          onClick={handleSamplePDF}
        >
          Load Sample PDF
        </button>
      </div>
    </div>
  );
}

export default HomePage;
