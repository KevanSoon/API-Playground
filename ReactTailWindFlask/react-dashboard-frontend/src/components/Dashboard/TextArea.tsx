"use client"
import React, { useState } from 'react'


const TextArea = ({onButtonClick,}: {
  onButtonClick: (value: string) => void;
}) => {
  const [textareaValue, setTextareaValue] = React.useState('');

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setTextareaValue(e.target.value); 
  };
  const handleButtonClick = () => {
    onButtonClick(textareaValue);
  };

  return <div className='sticky text-4 font-mono pt-4'>
    <div className='w-[800px] h-[115px] p-[20px] rounded-3xl border border-stone-300 shadow-xl flex flex-col '>
       <textarea value={textareaValue} onChange={handleTextareaChange} className='resize-none focus:outline-none w-full '></textarea>
       <button onClick={handleButtonClick} className="ml-auto w-[45px] h-[45px] bg-black text-white text-2xl rounded-full px-4 py-2 hover:bg-gray-800">↑</button>
    </div>
  </div>

}

export default TextArea
