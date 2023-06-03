import React,{ useRef, useEffect, useState, useMemo } from "react";
import PropTypes from "prop-types";
import { Line } from "react-chartjs-2";
import Card from "@mui/material/Card";
import ArgonBox from "components/ArgonBox";
import ArgonTypography from "components/ArgonTypography";
import gradientChartLine from "assets/theme/functions/gradientChartLine";
import configs from "bique_components/MonthCategoryChart/configs";
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import dayjs from 'dayjs';
import axios from "axios";
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import { UserContext } from 'UserContext';


const today = dayjs();
const yesterday = dayjs().subtract(1, 'day');
const todayStartOfTheDay = today.startOf('day');

import colors from "assets/theme/base/colors";
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

function MonthcategoryChart({ title, description, height }) {
    const chartRef = useRef(null);
    const [chartData, setChartData] = useState({});
    const { data, options } = chartData;
    const [selectedType, setSelectedType] = useState('income');
    const { userId, setUserId } = React.useContext(UserContext);

    async function fetchDataset(selectedType) {
        try {
            const response = await axios.get(`http://10.4.41.51:8000/get_category?category=${selectedType}&user_id=${userId}`);
            return response.data;
        } catch (error) {
            console.error("Error fetching dataset:", error);
            return null;
        }
    }

    useEffect(() => {
      const fetchData = async () => {
        const chart = await fetchDataset(selectedType);
        console.log(chart);
        if (chart) {
          const chartDatasets = chart.datasets.map((dataset) => ({
            ...dataset,
                tension: 0.4,
                pointRadius: 0,
                borderWidth: 3,
                borderColor: colors[dataset.color]
                    ? colors[dataset.color || "dark"].main
                    : colors.dark.main,
                fill: true,
                maxBarThickness: 6,
                backgroundColor: gradientChartLine(
                    chartRef.current.children[0],
                    colors[dataset.color] ? colors[dataset.color || "dark"].main : colors.dark.main
                ),
          }));

          setChartData(configs(chart.labels || [], chartDatasets));
        }
      };

      fetchData();
    }, [selectedType]);

    const handleChange = (event) => {
        setSelectedType(event.target.value);
    };

    const renderChart = useMemo(() => {
        // if (!data) {
        //     return null; // If chartData is empty, don't render anything
        // }

        return (
            <ArgonBox p={2}>
                {title || description ? (
                    <ArgonBox px={description ? 1 : 0} pt={description ? 1 : 0}>
                        {title && (
                            <ArgonBox mb={1}>
                                <ArgonTypography variant="h6">{title}</ArgonTypography>
                            </ArgonBox>
                        )}
                        <ArgonBox mb={1} sx={{ display: 'flex' }}>
                            <ArgonBox mb={2}>
                                <FormControl sx={{ m: 2, minWidth: 300, mr: 2 }}>
                                    <InputLabel id="demo-simple-select-helper-label">Expenditure</InputLabel>
                                    <Select
                                        labelId="demo-simple-select-helper-label"
                                        id="demo-simple-select-helper"
                                        value={selectedType}
                                        label="Expenditure"
                                        onChange={handleChange}
                                    >
                                        <MenuItem value="">
                                            <em>None</em>
                                        </MenuItem>
                                        {types.map((type) => (
                                            <MenuItem key={type} value={type}>
                                                {type}
                                            </MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                            </ArgonBox>
                        </ArgonBox>
                        <ArgonBox mb={2}>
                            <ArgonTypography component="div" variant="button" fontWeight="regular" color="text">
                                {description}
                            </ArgonTypography>
                        </ArgonBox>
                    </ArgonBox>
                ) : null}
                <ArgonBox ref={chartRef} sx={{ height }}>
                    <Line data={data} options={options} />
                </ArgonBox>
            </ArgonBox>
        );
    }, [chartData, height, description, selectedType]);

    return title || description ? <Card>{renderChart}</Card> : renderChart;
}

MonthcategoryChart.defaultProps = {
    title: "",
    description: "",
    height: "19.125rem",
};

MonthcategoryChart.propTypes = {
    title: PropTypes.string,
    description: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
    height: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    chart: PropTypes.objectOf(PropTypes.array).isRequired,
};

export default MonthcategoryChart;
