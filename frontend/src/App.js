import React, { useState } from 'react';
import Lottie from "lottie-react";
import Loading from "./loading.json";
import Learning from "./learning.json";
import Completed from "./completed.json";


function App() {
  const [inputValue, setInputValue] = useState('');
  const [downloadLink, setDownloadLink] = useState(null);
  const [processing, setProcessing] = useState(false);

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Show the processing button and hide the form content
    setProcessing(true);

    const url = '/check'; // Replace with your API endpoint

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: inputValue }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        // Create the download link
        const downloadLink = (
          <a
            href={url}
            download="output.xlsx"
            className="bg-blue-500 hover:bg-blue-600 text-white font-semibold p-2 rounded inline-block mt-4"
          >
            Download Excel File
          </a>
        );

        setDownloadLink(downloadLink);
      } else {
        // Handle HTTP errors
        console.error(`HTTP Error: ${response.status}`);
      }
    } catch (error) {
      // Handle network or other errors
      console.error(error);
    } finally {
      // Hide the processing button
      setProcessing(false);
    }
  };
  
  return (
    <div className="fixed top-0 left-0 h-screen w-screen bg-zinc-50 flex justify-center items-center text-black">
      {processing ? (
        <>
        <Lottie animationData={Loading} />
        <h3>Working hard, please wait...</h3>
        </>
      ) : (
        <>
          {downloadLink ? (
            <>
            <Lottie animationData={Completed} />
            <div>
              <h3>Finally, I'm done!!!</h3>
              {downloadLink}
            </div>
            </>
          ) : (
            <>
            <Lottie animationData={Learning} />
            <form onSubmit={handleSubmit} className="bg-white p-4 rounded-lg shadow-lg h-96 w-96 flex flex-col">
              <input
                type="text"
                name="input"
                id="input"
                value={inputValue}
                onChange={handleInputChange}
                className="border border-gray-300 rounded  px-0 py-0 h-full"
              />
              <button type="submit" className="mt-2 bg-blue-500 hover-bg-blue-600 text-white font-semibold p-2 rounded">
                Check
              </button>
              
            </form>
            </>
          )}
        </>
      )}
    </div>
  );
}

export default App;
