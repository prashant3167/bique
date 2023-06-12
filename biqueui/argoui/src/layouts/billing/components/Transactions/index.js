import React, { useEffect, useState } from 'react';
import Card from '@mui/material/Card';
import Icon from '@mui/material/Icon';
import ArgonBox from 'components/ArgonBox';
import ArgonTypography from 'components/ArgonTypography';
import Transaction from 'layouts/billing/components/Transaction';

function Transactions() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    fetch('http://10.4.41.51:8000/predicted_advisors/')
      .then(response => response.json())
      .then(data => setTransactions(data))
      .catch(error => console.error('Error fetching transactions:', error));
  }, []);

  return (
    <Card sx={{ height: '100%' }}>
      <ArgonBox display="flex" justifyContent="space-between" alignItems="center" pt={3} px={2}>
        <ArgonTypography variant="h6" fontWeight="medium" textTransform="capitalize">
          Recommended advisors
        </ArgonTypography>
        {/* <ArgonBox display="flex" alignItems="flex-start">
          <ArgonBox color="text" mr={0.5} lineHeight={0}>
            <Icon color="inherit" fontSize="small">
              date_range
            </Icon>
          </ArgonBox>
          <ArgonTypography variant="button" color="text" fontWeight="regular">
            23 - 30 March 2020
          </ArgonTypography>
        </ArgonBox> */}
      </ArgonBox>
      <ArgonBox pt={3} pb={2} px={2}>
        <ArgonBox mb={2}>
          {/* <ArgonTypography variant="caption" color="text" fontWeight="bold" textTransform="uppercase">
            newest
          </ArgonTypography> */}
        </ArgonBox>
        <ArgonBox component="ul" display="flex" flexDirection="column" p={0} m={0} sx={{ listStyle: 'none' }}>
          {transactions.map((transaction, index) => (
            <Transaction
              key={index}
              name={transaction.name}
              description=""
              value={transaction.rank}
            />
          ))}
        </ArgonBox>
      </ArgonBox>
    </Card>
  );
}

export default Transactions;
