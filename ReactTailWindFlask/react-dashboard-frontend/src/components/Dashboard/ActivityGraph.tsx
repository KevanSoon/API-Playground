"use client"

import React from 'react'
import { FiUser } from 'react-icons/fi'
import {
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid,
    Line,
    LineChart,
  } from "recharts";
  


const ActivityGraph = () => {
  const [chartData, setChartData] = React.useState([]);

 React.useEffect(() => {
    fetch('http://127.0.0.1:5000/chartdata')  // or full URL if no proxy
      .then((res) => res.json())
      .then((data) => {
        setChartData(data.chart_data);
      })
      .catch((err) => console.error('Error fetching chart data:', err));
  }, []);

  return <div className='col-span-8 overflow-hidden 
  rounded border border-stone-300'>
      <div className='p-4'>
        <h3 className='flex items-center gap-1.5 font medium'>
            <FiUser></FiUser> Activity
        </h3>
      </div>
      <div className='h-64 px-4'>
      <ResponsiveContainer width="100%" height="100%">
          <LineChart
            width={500}
            height={400}
            data={chartData}
            margin={{
              top: 0,
              right: 0,
              left: -24,
              bottom: 0,
            }}
          >
            <CartesianGrid stroke="#e4e4e7" />
            <XAxis
              dataKey="name"
              axisLine={false}
              tickLine={false}
              className="text-xs font-bold"
              padding={{ right: 4 }}
            />
            <YAxis
              className="text-xs font-bold"
              domain={[0, 60]}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              wrapperClassName="text-sm rounded"
              labelClassName="text-xs text-stone-500"
            />
            <Line
              type="monotone"
              dataKey="Minimum"
              stroke="#18181b"
              fill="#18181b"
            />
            <Line
              type="monotone"
              dataKey="Median"
              stroke="#5b21b6"
              fill="#5b21b6"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>

    

}

export default ActivityGraph
