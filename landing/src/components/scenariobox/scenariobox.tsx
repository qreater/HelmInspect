import { motion, AnimatePresence } from 'framer-motion'
import React, { useState, useEffect } from 'react'
import { ScenarioBox, ScenarioItem, HeroText } from '../index.styles'

interface Scenario {
    time?: string
    command: React.ReactNode
    message: React.ReactNode
}

interface AnimatedScenarioBoxProps {
    scenarios: Scenario[]
    intervalTime?: number
    restartDelay?: number
}

export default function AnimatedScenarioBox({
    scenarios,
    intervalTime = 2000,
    restartDelay = 5000,
}: AnimatedScenarioBoxProps) {
    const [currentIndex, setCurrentIndex] = useState(0)

    useEffect(() => {
        const interval = setTimeout(
            () => {
                setCurrentIndex((prev) => (prev + 1) % scenarios.length)
            },
            currentIndex === scenarios.length - 1 ? restartDelay : intervalTime,
        )

        return () => clearTimeout(interval)
    }, [scenarios.length, intervalTime, restartDelay, currentIndex])

    return (
        <ScenarioBox
            style={{
                position: 'relative',
            }}
        >
            <AnimatePresence mode="wait">
                {scenarios.map((scenario, index) => (
                    <motion.div
                        key={index}
                        style={{
                            opacity: 1,
                            marginBottom: '1rem',
                        }}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{
                            opacity: currentIndex >= index ? 1 : 0,
                            y: currentIndex >= index ? 0 : 20,
                        }}
                        exit={{
                            opacity: 0,
                            y: -20,
                        }}
                        transition={{ duration: 0.5 }}
                    >
                        <ScenarioItem>
                            {scenario.time ? (
                                <HeroText>
                                    {scenario.time} &gt; {scenario.command}
                                </HeroText>
                            ) : (
                                <HeroText>&gt; {scenario.command}</HeroText>
                            )}
                            <HeroText>{scenario.message}</HeroText>
                        </ScenarioItem>
                    </motion.div>
                ))}
            </AnimatePresence>
        </ScenarioBox>
    )
}
