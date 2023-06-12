import React, { useState, useEffect } from 'react';
import ArgonTypography from 'components/ArgonTypography';
import CategoriesList from 'examples/Lists/CategoriesList';
import { UserContext } from 'UserContext';

const CategoryData = () => {
  const [cdata, setData] = useState({});
  const [loading, setLoading] = useState(true);
  const { userId } = React.useContext(UserContext);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://10.4.41.51:8000/get_month_category/${userId}`);
        const data = await response.json();
        console.log(data); // Log the fetched data
        setData(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, [userId]);

  const categoriesListData = Object.entries(cdata).map(([name, spent]) => ({
    color: 'dark',
    icon: <i className="ni ni-mobile-button" style={{ fontSize: '12px' }} />,
    name: name, // Convert the key to a string if it's not already
    description: (
      <>
      {spent}
        {/* <ArgonTypography variant="caption" color="text" fontWeight="medium">
          {spent}
        </ArgonTypography> */}
      </>
    ),
    route: '/',
  }));

  return (
    <div>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <CategoriesList title="categories" categories={categoriesListData} />
      )}
    </div>
  );
};

export default CategoryData;
