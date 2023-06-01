// // MyComponent.js
// import React, { useContext } from 'react';
// import { UserContext } from './UserContext';

// const MyComponent = () => {
//   const { userId, setUserId } = useContext(UserContext);

//   // Use the userId and setUserId as needed

//   return (
//     <div>
//       <p>User ID: {userId}</p>
//       <button onClick={() => setUserId(123)}>Set User ID</button>
//     </div>
//   );
// };

// export default MyComponent;


import React, { useContext, useEffect, useState } from 'react';
// import { useHistory } from 'react-router-dom'; // Import useHistory from react-router-dom
import { UserContext } from './UserContext';
import { useNavigate, useLocation } from 'react-router-dom';
import TableContainer from "@mui/material/TableContainer";



const MyComponent = () => {
  // const history = useHistory(); // Get the history object
  const { userId, setUserId } = useContext(UserContext);
  const [selectedUserId, setSelectedUserId] = useState('');
  const [dropdownOptions, setDropdownOptions] = useState([]); // State to hold dropdown options

  const navigate = useNavigate();

  useEffect(() => {
    // Fetch the JSON file and extract the desired value
    fetch('accounts.json')
      .then((response) => response.json())
      .then((data) => {
        // Assuming the JSON file contains an array of user IDs
        console.log(data);
        setDropdownOptions(data); // Set the dropdown options with the user IDs from the JSON data
      })
      .catch((error) => {
        console.error('Error fetching JSON file:', error);
      });
  }, []);

  const handleSelectionChange = (e) => {
    setSelectedUserId(e.target.value);
  };

  const handleButtonClick = () => {
    setUserId(selectedUserId);
    // history.push('/another-page');
    navigate('/transactions');
  };

  return (
    <TableContainer>
      <p>User ID: {userId}</p>
      <select value={selectedUserId} onChange={handleSelectionChange}>
        <option value="">Select User ID</option>
        {dropdownOptions.map((option) => (
          <option key={option.name} value={option.id}>
            {option.name}
          </option>
        ))}
      </select>
      <button onClick={handleButtonClick}>Set User ID</button>
    </TableContainer>
  );
};

export default MyComponent;