import { useEffect, useRef, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './sidebar.scss';

const sidebarNavItems = [
    {
        display: 'Transactions',
        icon: <i className='bx bx-home'></i>,
        to: '/',
        section: ''
    },
    {
        display: 'Detailed Spending',
        icon: <i className='bx bx-star'></i>,
        to: '/started',
        section: 'started'
    },
    {
        display: 'Financial Advisor',
        icon: <i className='bx bx-calendar'></i>,
        to: '/calendar',
        section: 'calendar'
    },
    {
        display: 'Add Accounts',
        icon: <i className='bx bx-receipt'></i>,
        to: '/order',
        section: 'order'
    },
    {
        display: 'User',
        icon: <i className='bx bx-user'></i>,
        to: '/user',
        section: 'user'
    }
]

const Sidebar = () => {
    const [activeIndex, setActiveIndex] = useState(0);
    const [stepHeight, setStepHeight] = useState(0);
    const [isCollapsed, setIsCollapsed] = useState(false); // State variable for collapse status
    const sidebarRef = useRef();
    const indicatorRef = useRef();
    const location = useLocation();
  
    useEffect(() => {
      setTimeout(() => {
        const sidebarItem = sidebarRef.current.querySelector('.sidebar__menu__item');
        indicatorRef.current.style.height = `${sidebarItem.clientHeight}px`;
        setStepHeight(sidebarItem.clientHeight);
      }, 50);
    }, []);
  
    useEffect(() => {
      const curPath = window.location.pathname.split('/')[1];
      const activeItem = sidebarNavItems.findIndex((item) => item.section === curPath);
      setActiveIndex(curPath.length === 0 ? 0 : activeItem);
    }, [location]);
  
    const toggleCollapse = () => {
      setIsCollapsed(!isCollapsed);
    };
  
    return (
      <div className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
        <div className="sidebar__logo">Bique</div>
        <div ref={sidebarRef} className="sidebar__menu">
          <div
            ref={indicatorRef}
            className="sidebar__menu__indicator"
            style={{
              transform: `translateX(-50%) translateY(${activeIndex * stepHeight}px)`,
            }}
          ></div>
          {sidebarNavItems.map((item, index) => (
            <Link to={item.to} key={index}>
              <div className={`sidebar__menu__item ${activeIndex === index ? 'active' : ''}`}>
                <div className="sidebar__menu__item__icon">{item.icon}</div>
                <div className="sidebar__menu__item__text">{item.display}</div>
              </div>
            </Link>
          ))}
        </div>
        <button className="sidebar__toggle" onClick={toggleCollapse}>
          {isCollapsed ? 'Expand' : 'Collapse'}
        </button>
      </div>
    );
  };
  
  export default Sidebar;