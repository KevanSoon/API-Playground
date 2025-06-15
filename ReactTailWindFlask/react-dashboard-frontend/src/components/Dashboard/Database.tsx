import React, { useEffect, useState } from 'react';

const SupabaseInfoComponent = () => {
  const [data, setData] = useState<{ role: string; text: string }[] | null>(null);

  useEffect(() => {
    fetch('http://localhost:5000/supabase-info')
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  if (!data) return <p>Loading...</p>;

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-2">Chat History</h1>
      <ul className="space-y-2">
        {data.map((entry, index) => (
          <li key={index} className={`p-2 rounded ${
            entry.role === 'user' ? 'bg-blue-100 text-blue-800 self-end' : 'bg-gray-200 text-gray-900 self-start'
          }`}>
            <strong>{entry.role === 'user' ? 'User:' : 'Bot:'}</strong> {entry.text}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SupabaseInfoComponent;
