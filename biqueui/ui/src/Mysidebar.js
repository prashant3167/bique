import { Sidebar, Menu, MenuItem } from 'react-pro-sidebar';
import { Link } from 'react-router-dom';


const Mysidebar = () => {
  return (
    <Sidebar>
  <Menu>
    <MenuItem> Documentation</MenuItem>
    <MenuItem > Calendar</MenuItem>
    <MenuItem> E-commerce</MenuItem>
  </Menu>
</Sidebar>
  );
};

export default Mysidebar;