"use client"

import { useRouteStore } from '@/store/useRouteStore'
import React from 'react'
import { IconType } from 'react-icons'
import { FiHome,  FiUsers } from 'react-icons/fi'
import { FaMap } from "react-icons/fa";
import { TbMessageChatbot } from "react-icons/tb";



const RouteSelect = () => {
  const {selectedRoute, setSelectedRoute} = useRouteStore()
  return <div className='space-y-1'>
        <Route onClick={() => setSelectedRoute("Dashboard")} Icon={FiHome} selected={selectedRoute === "Dashboard"} title="Dashboard"></Route>
        <Route onClick={() => setSelectedRoute("Chatbot")} Icon={TbMessageChatbot} selected={selectedRoute === "Chatbot"} title="Chatbot"></Route>
        <Route onClick={() => setSelectedRoute("Map")} Icon={FaMap} selected={selectedRoute === "Map"} title="Map"></Route>
        <Route onClick={() => setSelectedRoute("RMap")} Icon={FaMap} selected={selectedRoute === "RMap"} title="Rainfall Map"></Route>
        <Route onClick={() => setSelectedRoute("Database")} Icon={FaMap} selected={selectedRoute === "Database"} title="Supabase Information"></Route>
    
        
  </div>
}


export default RouteSelect

const Route = ({
    selected,
    Icon,
    title,
    onClick,

}: {
    selected: boolean;
    Icon: IconType;
    title: string;
    onClick: () => void;
}) => {
    return <button onClick={onClick}
    className={`flex items-center justify-start gap-2 w-full
    rounded px-2 py-1.5 text-sm transition-[box-shadow,_background-color,
    _color] ${selected 
        ? "bg-white text-stone-950 shadow"
    : "hover:bg-stone-200 bg-transparent text-stone-500 shadow-none"
    }`}>
        <Icon className={selected ? "text-violet-500" : ""}></Icon>
        <span>{title}</span>
    </button>
} 

