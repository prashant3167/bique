/* eslint-disable no-unused-vars */
/**
=========================================================
* Argon Dashboard 2 MUI - v3.0.1
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-dashboard-material-ui
* Copyright 2023 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// @mui material components
import Grid from "@mui/material/Grid";
import Icon from "@mui/material/Icon";

// Argon Dashboard 2 MUI components
import ArgonBox from "components/ArgonBox";
import ArgonTypography from "components/ArgonTypography";

// Argon Dashboard 2 MUI example components
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import DetailedStatisticsCard from "examples/Cards/StatisticsCards/DetailedStatisticsCard";
import SalesTable from "examples/Tables/SalesTable";
import CategoriesList from "examples/Lists/CategoriesList";
import GradientLineChart from "examples/Charts/LineCharts/GradientLineChart";
import VerticalBarChart from "examples/Charts/BarCharts/VerticalBarChart";

import MonthcategoryChart from "bique_components/MonthCategoryChart";


// Argon Dashboard 2 MUI base styles
import typography from "assets/theme/base/typography";

// Dashboard layout components
import Slider from "layouts/dashboard/components/Slider";

// Data
import gradientLineChartData from "layouts/dashboard/data/gradientLineChartData";
import salesTableData from "layouts/dashboard/data/salesTableData";
import categoriesListData from "layouts/dashboard/data/categoriesListData";
import useUserIdCheck from 'useUserIdCheck';
import { UserContext } from 'UserContext';

import { useState, useEffect,useContext } from 'react';
import axios from 'axios';

const types = [
  "groceries",
  "entertainment",
  "shopping",
  "utilities",
  "travel",
  "food delivery",
  "transfer",
  "income",
  "refund",
  "other",
];
const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

function Default() {
  useUserIdCheck();
  const { size } = typography;
  const [selectedType, setSelectedType] = useState('');
  const [selectedMonth, setSelectedMonth] = useState('');
  const [selectedYear, setSelectedYear] = useState('');
  const [chartData, setChartData] = useState(null);
  const [transaction, setTransaction] = useState({spend: 213,income:323, totaltransaction:434});
  const { userId, setUserId } = useContext(UserContext);


  useEffect(() => {
    // Function to fetch chart data from the API based on selected options
    const fetchChartData = async () => {
      try {
        const response = await axios.get(`/api/chart-data?type=${selectedType}&month=${selectedMonth}&year=${selectedYear}`);
        setChartData(response.data);
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    };

    if (selectedType && selectedMonth && selectedYear) {
      fetchChartData();
    }
  }, [selectedType, selectedMonth, selectedYear]);

  useEffect(() => {
    // Perform some other side effect or subscribe to an event
    // This effect only runs on component mount
    const fetchDashboardData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/get_dashboard/${userId}`);
        setTransaction(response.data);
        console.log(response.data);
      } catch (error) {
        console.error('Error fetching chart data:', error);
      }
    };
    if (userId) {
      fetchDashboardData();
    }
    
  }, []);

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <ArgonBox py={3}>
        <Grid container spacing={3} mb={3}>
          <Grid item xs={12} md={6} lg={3}>
            <DetailedStatisticsCard
              title="Money Spent in Month"
              count={"€" +transaction.spend}
              icon={{ color: "info", component: <i className="ni ni-money-coins" /> }}
              // percentage={{ color: "success", count: "+55%", text: "since yesterday" }}
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <DetailedStatisticsCard
              title="Safe to spend"
              count={"€" +transaction.income}
              icon={{ color: "error", component: <i className="ni ni-world" /> }}
              percentage={{ color: "success", count: "+3%", text: "since last week" }}
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <DetailedStatisticsCard
              title="new clients"
              count={"€" +transaction.income}
              icon={{ color: "success", component: <i className="ni ni-paper-diploma" /> }}
              percentage={{ color: "error", count: "-2%", text: "since last quarter" }}
            />
          </Grid>
          <Grid item xs={12} md={6} lg={3}>
            <DetailedStatisticsCard
              title="sales"
              count="$103,430"
              icon={{ color: "warning", component: <i className="ni ni-cart" /> }}
              percentage={{ color: "success", count: "+5%", text: "than last month" }}
            />
          </Grid>
        </Grid>
        <Grid container spacing={3} mb={3}>
      {/* <Grid item xs={12} lg={7}>
        <GradientLineChart
          title="Sales Overview"
          description=""
          chart={gradientLineChartData}
        />        
      </Grid> */}
      <Grid item xs={12} lg={7}>
        <MonthcategoryChart
          title="Monthly Spending Trending on different categories"
          description=""
          // chart={gradientLineChartData}
        />        
      </Grid>
      <Grid item xs={12} lg={5}>
            {/* <Slider /> */}
            <VerticalBarChart
  title="Vertical Bar Chart"
  chart={{
    labels: ["16-20", "21-25", "26-30", "31-36", "36-42", "42+"],
    datasets: [{
      label: "Sales by age",
      color: "dark",
      data: [15, 20, 12, 60, 20, 15],
    }],
  }}
/>
          </Grid>
    </Grid>
        <Grid container spacing={3} mb={3}>
          <Grid item xs={12} lg={7}>
            <GradientLineChart
              title="Sales Overview"
              description={
                <ArgonBox display="flex" alignItems="center">
                  <ArgonBox fontSize={size.lg} color="success" mb={0.3} mr={0.5} lineHeight={0}>
                    <Icon sx={{ fontWeight: "bold" }}>arrow_upward</Icon>
                  </ArgonBox>
                  <ArgonTypography variant="button" color="text" fontWeight="medium">
                    4% more{" "}
                    <ArgonTypography variant="button" color="text" fontWeight="regular">
                      in 2022
                    </ArgonTypography>
                  </ArgonTypography>
                </ArgonBox>
              }
              chart={gradientLineChartData}
            />
          </Grid>
          
        </Grid>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <SalesTable title="Sales by Country" rows={salesTableData} />
          </Grid>
          <Grid item xs={12} md={4}>
            <CategoriesList title="categories" categories={categoriesListData} />
          </Grid>
        </Grid>
      </ArgonBox>
      {/* <Footer /> */}
    </DashboardLayout>
  );
}

export default Default;
