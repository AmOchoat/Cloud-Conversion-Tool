import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/auth-context';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [form, setForm] = useState({});
  const { accessToken } = useContext(AuthContext);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setForm((prevState) => ({ ...prevState, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', file);
    Object.entries(form).forEach(([key, value]) => {
      formData.append(key, value);
    });
    for (var pair of formData.entries()) {
      console.log(pair[0] + ', ' + pair[1]);
    }
    console.log('token', accessToken);
    try {
      const response = await fetch('http://35.237.111.106:8000/api/tasks', {
        method: 'POST',
        body: formData,
        headers: {
          // 'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (response.ok) {
        console.log('File uploaded successfully.');
      } else {
        console.error('Failed to upload file.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="file">Select a file:</label>
        <input type="file" id="file" name="file" onChange={handleFileChange} />
      </div>
      <div>
        <label htmlFor="nombre">nombre: </label>
        <input
          type="text"
          id="nombre"
          name="nombre"
          onChange={handleInputChange}
        />
      </div>
      <div>
        <label htmlFor="extension_convertir">extension convertir: </label>
        <input
          type="text"
          id="extension_convertir"
          name="extension_convertir"
          onChange={handleInputChange}
        />
      </div>
      <button type="submit">Submit</button>
    </form>
  );
}

export default UploadForm;
