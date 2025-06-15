"use client"

import React, { useState, useEffect } from 'react'

const TypingDiv = ({ text = '', typingSpeed = 100 }: TypingDivProps) => {
  const [displayedText, setDisplayedText] = useState<string>('')

  useEffect(() => {
    let isCancelled = false

    const typeCharacter = (index: number) => {
      if (isCancelled) return
      if (index < text.length) {
        setDisplayedText((prev) => prev + text[index])
        setTimeout(() => typeCharacter(index + 1), typingSpeed)
      }
    }

    setDisplayedText('') // Reset text
    typeCharacter(0)     // Start typing from index 0

    return () => {
      isCancelled = true // Clean up on unmount or text change
    }
  }, [text, typingSpeed])

  return (
    <div className="text-xl font-mono text-gray-800 ">
      {displayedText}
      <span className="animate-pulse">|</span>
    </div>
  )
}

export default TypingDiv

type TypingDivProps = {
  text?: string
  typingSpeed?: number
}
