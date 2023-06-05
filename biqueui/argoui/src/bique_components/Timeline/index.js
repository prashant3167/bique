import React, { useEffect, useState } from "react";
import TimelineList from "examples/Timeline/TimelineList";
import TimelineItem from "examples/Timeline/TimelineItem";

const TransactionTimeline = () => {
  const [timelineData, setTimelineData] = useState([]);

  useEffect(() => {
    // Fetch data from the API
    fetchDataFromAPI()
      .then((data) => {
        setTimelineData(data);
      })
      .catch((error) => {
        console.error("Error fetching data from API:", error);
      });
  }, []);

  const fetchDataFromAPI = async () => {
    try {
      // Make API call and get the timeline data
      const response = await fetch("http://10.4.41.51:8000/get_daily_transaction/${userId}");
      const data = await response.json();
      return data;
    } catch (error) {
      throw new Error("Failed to fetch data from API");
    }
  };

  return (
    <TimelineList title="Timeline">
      {timelineData.map((item) => (
        <TimelineItem
          key={item.id}
          color={item.color}
          icon={item.icon}
          title={item.title}
          dateTime={item.dateTime}
          description={item.description}
          badges={item.badges}
          lastItem={item.lastItem}
        />
      ))}
    </TimelineList>
  );
};

export default TransactionTimeline;
