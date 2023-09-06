import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import { Helmet } from 'react-helmet-async';
import Button from 'react-bootstrap/Button';
import Axios from 'axios';
import { toast } from 'react-toastify';
import React, { Component } from 'react';
//import results from './public/plagiarism/results';

export default function UploadScreen() {
  const uploadFileHandler = (e) => {
    console.log('UploadHander check');
    const source_file = e.target.files[0];
    const target_file = e.target.files[1];
    const formData = new FormData();
    formData.append('source_file', source_file);
    console.log(source_file);
    formData.append('target_file', target_file);
    console.log(target_file);
    console.log(Object.fromEntries(formData.entries()));

    Axios.post(
      'http://localhost:8000/detect_plagiarism/upload_files/',
      formData
    );
    //console.log('It works');
    //toast.success('Files uploaded successfully!');
    //toast.error('Something went wrong!');
    //console.error();
    //const results = require('studybank/plagiarism/uploads/results.json');

    //console.log(results);
    //console.log(results[0].source_percent);
  };
  fetch('./plagiarism/results.json')
    .then((response) => {
      console.log(response);
      return response.json();
    })
    .then((data) => {
      console.log(data);
    })
    .catch((err) => {
      console.log('Error reading results file ' + err);
    });
  return (
    <Container className="small-container">
      <Helmet>
        <title>Upload Files</title>
      </Helmet>
      <h1>Upload Files for Plagiarism Detection</h1>
      <Form>
        <Form.Group className="mb-3" controlId="formFileMultiple">
          <Form.Label>Upload source and target files</Form.Label>
          <Form.Control type="file" multiple onChange={uploadFileHandler} />
        </Form.Group>
        <div className="mb-3">
          <Button type="submit">Upload</Button>
        </div>
      </Form>
      <link></link>
    </Container>
  );
}
