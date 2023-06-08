// @mui material components
import Card from "@mui/material/Card";

// Argon Dashboard 2 MUI components
import ArgonBox from "components/ArgonBox";
import ArgonTypography from "components/ArgonTypography";

// Billing page components
import Bill from "layouts/billing/components/Bill";
import React,{ useState, useEffect } from "react";
import { UserContext } from 'UserContext';

function BillingInformation() {
  const [advisors, setBills] = useState([]);
  const { userId, setUserId } = React.useContext(UserContext);

  useEffect(() => {
    // Fetch bills from the API
    fetch(`http://10.4.41.51:8000/advisors/${userId}`)
      .then((response) => response.json())
      .then((data) => setBills(data))
      .catch((error) => console.error(error));
  }, []);

  return (
    <Card id="delete-account">
      <ArgonBox pt={3} px={2}>
        <ArgonTypography variant="h6" fontWeight="medium">
          Hired Advisor
        </ArgonTypography>
      </ArgonBox>
      <ArgonBox pt={1} pb={2} px={2}>
        <ArgonBox component="ul" display="flex" flexDirection="column" p={0} m={0}>
          {advisors.map((advisor, index) => (
            <Bill
              key={index}
              name={advisor.name}
              date={advisor.date}
              rating={advisor.rating}
              noGutter={index === advisors.length - 1}
            />
          ))}
        </ArgonBox>
      </ArgonBox>
    </Card>
  );
}

export default BillingInformation;
