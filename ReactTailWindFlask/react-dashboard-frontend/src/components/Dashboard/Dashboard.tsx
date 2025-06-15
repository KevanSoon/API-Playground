"use client"

import React, { useState } from 'react'
import TopBar from './TopBar'
import Grid from './Grid'
import Map from './Map'
import RMap from './RMap'
import { useRouteStore } from '@/store/useRouteStore'
import Chatbot from './Chatbot'
import Database from './Database'


const Dashboard = () => {

  const {selectedRoute} = useRouteStore()

  return (
    <div className='bg-white rounded-lg pb-4 shadow'>
        {selectedRoute === 'Dashboard' &&    <TopBar></TopBar>}
        {selectedRoute === 'Dashboard' &&   <Grid></Grid>}
        {selectedRoute === 'Chatbot' &&   <Chatbot></Chatbot>}
        {selectedRoute === 'Map' && <Map></Map>}
        {selectedRoute === 'RMap' && <RMap></RMap>}
        {selectedRoute === 'Database' && <Database></Database>}
    </div>
  )
}




export default Dashboard
