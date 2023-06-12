import React, { useContext, useEffect, useState } from 'react';
import './MyComponent.scss'; // Path to your CSS file
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import InputLabel from '@mui/material/InputLabel';
import OutlinedInput from '@mui/material/OutlinedInput';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { UserContext } from './UserContext';
import { useNavigate } from 'react-router-dom';
import TableContainer from "@mui/material/TableContainer";


const MyComponent = () => {
  const [open, setOpen] = useState(true);
  const { userId, setUserId } = useContext(UserContext);
  const [selectedUserId, setSelectedUserId] = useState('');
  const [dropdownOptions, setDropdownOptions] = useState([]);

  const navigate = useNavigate();

  useEffect(() => {
    fetch('accounts.json')
      .then((response) => response.json())
      .then((data) => {
        setDropdownOptions(data);
      })
      .catch((error) => {
        console.error('Error fetching JSON file:', error);
      });
  }, []);

  const handleChange = (event) => {
    setSelectedUserId(event.target.value);
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleOk = () => {
    setOpen(false);
    setUserId(selectedUserId);
    navigate('/Transactions');
  };

  const handleClose = () => {
    setOpen(true);
    setSelectedUserId("");
  };
  return (
    <div>
      {/* <div>{userId}</div> */}
      {/* <Button onClick={handleClickOpen}>Open select dialog</Button> */}
      <Dialog disableEscapeKeyDown open={open} onClose={handleClose}>
        <DialogTitle>Login</DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ display: 'flex', flexWrap: 'wrap' }}>
            <FormControl sx={{ m: 1, minWidth: 120 }}>
              <InputLabel htmlFor="demo-dialog-native"></InputLabel>
              <Select
                native
                value={selectedUserId}
                onChange={handleChange}
                input={<OutlinedInput label="selectedUserId" id="demo-dialog-native" />}
              >
                <option aria-label="None" value="" />
                {dropdownOptions.map((option) => (
                  <option key={option.name} value={option.id}>
                    {option.name}
                  </option>
                ))}
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleOk}>Ok</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default MyComponent;
