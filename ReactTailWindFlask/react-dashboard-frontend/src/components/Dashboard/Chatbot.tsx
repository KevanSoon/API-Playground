import React, { useEffect, useState } from 'react'
import Introduction from './Introduction'
import TextArea from './TextArea'
import Chatbox from './Chatbox';
import Loading from './Loading';
import TypingDiv from './TypingDiv';


interface ChatEntry {
    role: 'user' | 'bot';
    text: string
}


const Chatbot = () => {
    //state to control which component to display
    // const [showNewComponent, setShowNewComponent] = useState(false);
    // const [showResult, setResult] = useState(false);
    // const [textInput, setTextInput] = useState('');
    // const [response, setResponse] = useState("");
    const [chatHistory, setChatHistory] = useState<ChatEntry[]>([]);
    const [loading, setLoading] = useState(false);

    
    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const res = await fetch ('http://localhost:5000/supabase-info');
                const data = await res.json()
                setChatHistory(data.history)
            } catch (error) {
                console.error('Failed to fetch chat history: ', error);
            }
        };
        fetchHistory();
    }, []);


    const handleButtonClick = async (text: string) => {
        //set the input text and toggle the componenet visibility
        // setTextInput(text);
        // setShowNewComponent(true);
        // setResult(false)
        const newHistory: ChatEntry[] = [...chatHistory, { role: "user", text }];
        setChatHistory(newHistory);
        setLoading(true);

        try {
            const res = await fetch('http://localhost:5000/gemini-response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({text}),
            });
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await res.json();
            // setResult(true);
            // setResponse(data.result);
            setChatHistory([...newHistory, { role: "bot", text: data.result }]);
        } catch (error) {
            // setResult(true);
            console.error('Error fetching response',error);
            setChatHistory([...newHistory, { role: "bot", text: '⚠️ Error contacting server' }]);
            // setResponse('An error occurred while contacting the server');
        } finally {
            setLoading(false);
        }
    }

    return   <div className="flex flex-col items-center justify-center h-screen w-full">
        <div className="w-full max-w-[700px] overflow-y-auto p-4">
            {/* {showNewComponent && <Chatbox text={textInput}></Chatbox>}
            {showNewComponent && showResult && <TypingDiv text={response} typingSpeed={20} />}
            {showNewComponent && !showResult && <Loading></Loading>} */}
             
             {chatHistory.map((entry, index) =>
          entry.role === 'user' ? (
            <Chatbox key={index} text={entry.text} />
          ) : (
            <TypingDiv key={index} text={entry.text} typingSpeed={20} />
          )
        )}
        {loading && <Loading />}
        </div>
        {chatHistory.length === 0 && !loading && <Introduction />}
        {/* {!showNewComponent && <Introduction></Introduction>} */}
        <TextArea onButtonClick={handleButtonClick}></TextArea>
    </div>
}

export default Chatbot
