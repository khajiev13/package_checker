import React, { useState } from 'react';

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
        <div class="flex">
          <div class="relative">
            <div class="w-12 h-12 rounded-full absolute border-8 border-solid border-gray-200"></div>
            <div class="w-12 h-12 rounded-full animate-spin absolute border-8 border-solid border-purple-500 border-t-transparent"></div>
          </div>
        </div>
      ) : (
        <>
          {downloadLink ? (
            <div>
              <p>File is ready for download:</p>
              {downloadLink}
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="bg-white p-4 rounded-lg shadow-lg">
              <input
                type="text"
                name="input"
                id="input"
                value={inputValue}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <button type="submit" className="mt-2 bg-blue-500 hover-bg-blue-600 text-white font-semibold p-2 rounded">
                Check
              </button>
            </form>
          )}
        </>
      )}
    </div>
  );
}

export default App;
