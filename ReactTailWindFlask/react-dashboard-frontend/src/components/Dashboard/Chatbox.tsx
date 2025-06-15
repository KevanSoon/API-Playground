import React from 'react'

const Chatbox = ({text}: {text: string;}) => {
  return    <div className="p-4 flex justify-end w-full  ">
      <div className="p-4 bg-gray-100 rounded-2xl ml-auto ">
        <p>{text}</p>
      </div>
    </div>
}

export default Chatbox
