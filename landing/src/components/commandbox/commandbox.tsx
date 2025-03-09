import { useState } from 'react'
import { CodeParagraph } from '../index.styles'
import {
    CommandBoxCopied,
    CommandBoxCopy,
    CommandBoxIcon,
    CommandBoxWrapper,
} from './commandbox.styles'
import { AnimatePresence, motion } from 'framer-motion'

interface CommandBoxProps {
    children: React.ReactNode
    copyText: string
}

const CommandBox = ({ children, copyText }: CommandBoxProps) => {
    const [copied, setCopied] = useState(false)

    const copyCommand = () => {
        navigator.clipboard.writeText(copyText)

        if (copied) return
        setCopied(true)
        setTimeout(() => {
            setCopied(false)
        }, 1500)
    }

    return (
        <CommandBoxWrapper onClick={copyCommand}>
            <CodeParagraph>{children}</CodeParagraph>
            <CommandBoxIcon>
                <AnimatePresence mode="wait">
                    {copied ? (
                        <motion.div
                            key="copied"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            transition={{ duration: 0.1 }}
                        >
                            <CommandBoxCopied />
                        </motion.div>
                    ) : (
                        <motion.div
                            key="copy"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            transition={{ duration: 0.1 }}
                        >
                            <CommandBoxCopy />
                        </motion.div>
                    )}
                </AnimatePresence>
            </CommandBoxIcon>
        </CommandBoxWrapper>
    )
}

export default CommandBox
