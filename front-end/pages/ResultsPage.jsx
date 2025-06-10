import React from "react";

function ResultsPage() {
  const mcqs = [
    {
      question: "What is the capital of France?",
      options: ["Berlin", "Madrid", "Paris", "Rome"],
      answer: "Paris",
    },
    {
      question: "Which planet is known as the Red Planet?",
      options: ["Earth", "Mars", "Jupiter", "Saturn"],
      answer: "Mars",
    },
  ];
  return (
    <>
      <div>
        <h1 className="text-3xl text-stone-700 font-bold m-7">PDFAtoZ</h1>
      </div>
      <div className="flex justify-center ml-[170px] mt-[100px] mb-10">
        <div className="flex flex-col items-center mt-10">
          <div className="flex items-center">
            <h2 className="text-2xl font-semibold mb-4 text-gray-800">MCQ's</h2>
          </div>
          <div className="flex justify-center mb-4">
            <div className="w-[800px] max-w-3xl bg-white shadow-xl rounded-2xl p-12">
              {mcqs.map((mcq, index) => (
                <div
                  key={index}
                  className="mb-8 p-6 rounded-xl border border-gray-200 bg-gradient-to-br from-gray-50 to-gray-100 shadow-sm"
                >
                  <h3 className="text-md font-bold mb-4 text-gray-700 flex items-center gap-2">
                    <span className="w-12 h-8 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center font-bold text-base">
                      {index + 1}
                    </span>
                    {mcq.question}
                  </h3>
                  <ul className="flex flex-wrap justify-center gap-8 mb-2">
                    {mcq.options.map((option, i) => (
                      <li
                        key={i}
                        className={`px-8 py-2 rounded-lg border text-base transition
                      ${
                        option === mcq.answer
                          ? "bg-green-50 border-green-400 text-green-700 font-semibold"
                          : "bg-gray-50 border-gray-300 text-gray-700 hover:bg-indigo-50"
                      }
                    `}
                      >
                        {option}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
              <div className="mt-8 border-t pt-4">
                <h4 className="text-lg font-semibold mb-2 text-gray-700">
                  Answers
                </h4>
                <ul className="list-decimal pl-5">
                  {mcqs.map((mcq, idx) => (
                    <li key={idx} className="mb-1 text-green-700 font-semibold">
                      {mcq.answer}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default ResultsPage;
