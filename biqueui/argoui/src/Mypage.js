import React from 'react';
import PageLayout from "examples/LayoutContainers/PageLayout";
// import RTL from "layouts/billing/components/rtl";


import MyComponent from './MyComponent';

const MyPage = () => {
  return (
    <PageLayout >
      {/* <h1>My Page</h1> */}
      <MyComponent />
    </PageLayout>
  );
};

export default MyPage;
