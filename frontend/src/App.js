import axios from 'axios';
import React, { Component } from 'react';
import './App.css';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';


class App extends Component {

  state = {
    sku: '',
    name: '',
    description: '',
    products: {},
    productsList: [],
    alert: {
      showAlert: false,
      severity: "",
      alertTitle: "",
      alertDetail: "",
    },
    file: ''
  }

  handleSubmit = event => {
    if (!this.state.sku) {
      this.setState({
        ...this.state,
        alert: {
          showAlert: true,
          severity: 'error',
          alertTitle: 'Error',
          alertDetail: 'Please fill in the SKU field!'
        }
      });
    } else if (!this.state.name) {
      this.setState({
        ...this.state,
        alert: {
          showAlert: true,
          severity: 'error',
          alertTitle: 'Error',
          alertDetail: 'Please fill in the Name field!'
        }
      });
    } else if (!this.state.description) {
      this.setState({
        ...this.state,
        alert: {
          showAlert: true,
          severity: 'error',
          alertTitle: 'Error',
          alertDetail: 'Please fill in the Description field!'
        }
      });
    } else {
      axios.post(
        `http://localhost:8000/api/v1/products/`,
        {
          sku: this.state.sku,
          name: this.state.name,
          description: this.state.description
        }).then(response => this.setState({
          ...this.state,
          alert: {
            showAlert: true,
            severity: 'success',
            alertTitle: 'Hooray!!!',
            alertDetail: 'Product successfully created!'
          }
        }))
    }
  }

  handleFetchProducts = () => {
    axios.get(`http://localhost:8000/api/v1/products/products/`)
    .then(response => this.setState({
      ...this.state,
      products: response.data,
      productsList: response.data.results
    })).catch(err => console.log(err))
  }

  handleChange = event => {
    this.setState({
      ...this.state,
      [event.target.name]: event.target.value,
    });
  }

  handleFileUpload = async (event) => {
    await this.setState({
      ...this.state,
      file: event.target.files[0]
    });
    this.handleSubmitFile();
  }

  handleSubmitFile = () => {
    axios.post(
      `http:/localhost:8000/api/v1/products/upload/`,
      {file: this.state.file}
      )
      .then(response => this.setState({
        ...this.state,
        taskId: response.data.task_id
      }))
  }

  handleUploadProgress = () => {
    axios.get(
      `http://localhost:8000/api/v1/task-progress/` + this.state.taskId
      ).then(response => this.setState({
        ...this.state,
        taskProgress: response
    })
    ).catch(err => {
      this.setState({
        ...this.state,
        alert: {
          showAlert: true,
          severity: 'error',
          alertTitle: 'Oops!!!',
          alertDetail: 'An error occurred while trying to track your upload progress!'
        }
      })
    })
  }

  clearAlert = () => {
    setTimeout(() => {
      this.setState({
        ...this.state,
        alert: {
          showAlert: false,
          severity: "",
          alertTitle: "",
          alertDetail: "",
        },
      });
    }, 5000);

  }

  render() {
    return (
      <div className="App">
        {this.state.alert.showAlert && (
            <Alert
              severity={this.state.alert.severity}
              onClose={this.clearAlert()}
            >
              <AlertTitle>{this.state.alert.alertTitle}</AlertTitle>
              {this.state.alert.alertDetail}
            </Alert>
          )
        }
        <Box
          component="form"
          sx={{
            '& > :not(style)': { m: 1, width: '25ch' },
            margin: '5% auto'
          }}
          autoComplete="off"
        >
          <TextField id="outlined-basic" label="SKU" variant="outlined" name="sku" onChange={this.handleChange} required/><br/><br/>
          <TextField id="filled-basic" label="Name" variant="outlined" name="name" onChange={this.handleChange} required/><br/><br/>
          <TextField id="standard-basic" label="Description" variant="outlined" name="description" onChange={this.handleChange} required/><br/><br/>          
          <Button variant="contained" startIcon={<AddCircleIcon/>} onClick={this.handleSubmit}>Add Product</Button><br/><br/>
          <p style={{margin: 'auto'}}>Or Upload a batch of products</p><br/><br/>
          <input
            accept="image/*"
            style={{display: 'None'}}
            id="drForm"
            multiple
            type="file"
            onChange={this.handleUploadImage}
            required={true}
          />
          <label htmlFor="drForm">
            <Button
              color="primary"
              component="span"
              startIcon={<CloudUploadIcon />}
              onClick={this.handleFileUpload}
            >
              Upload Product CSV
            </Button>
          </label>
          <span>{this.state.file.name}</span>

        </Box>
      </div>
    );
  }
}

export default App;
