import React, { useState } from 'react';

function Animals() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [predictedAnimal, setPredictedAnimal] = useState(null);
  const [isLoadingPredictions, setIsLoadingPredictions] = useState(false);

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    setSelectedImage(file);
    setPredictedAnimal(null);
  };

  const handleSubmit = () => {
    const formData = new FormData();
    formData.append('image', selectedImage);
    setIsLoadingPredictions(true);
    fetch(`https://${process.env.REACT_APP_SERVE_URL}/classification`, {
      method: 'POST',
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        setIsLoadingPredictions(false);
        setPredictedAnimal(data.prediction);
        console.log('data', data);
      })
      .catch((err) => {
        setIsLoadingPredictions(false);
        console.error('Error fetching predictions', err);
      });
  };

  return (
    <div className='w-2/3 mx-auto pt-8'>
      <h1 className='text-2xl font-bold mb-4'>Animal Prediction</h1>
      <div className='flex'>
        <form>
          <input type='file' accept='image/*' onChange={handleImageChange} />
          {selectedImage && <img src={URL.createObjectURL(selectedImage)} alt='Selected' />}
          <br />
          <button
            type='button'
            className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 mt-4 rounded'
            onClick={handleSubmit}
          >
            Submit
          </button>
          {isLoadingPredictions && <p>Loading predictions...</p>}
          {predictedAnimal && <p>Predicted animal: {predictedAnimal}</p>}
        </form>
      </div>
    </div>
  );
}

export default Animals;
