import { useEffect, useContext } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { UserContext } from './UserContext';

const useUserIdCheck = () => {
  const { userId } = useContext(UserContext);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    if (!userId && location.pathname !== '/login') {
      navigate('/login'); // Navigate to the page where userId can be set
    }
  }, [userId, location, navigate]);
};

export default useUserIdCheck;
