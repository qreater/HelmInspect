import { CheckCircle, DocumentDuplicate } from '@styled-icons/heroicons-solid'
import styled from 'styled-components'

export const CommandBoxWrapper = styled.div`
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 3.5rem;

    max-width: 30rem;
    margin: 0 auto;
    padding: 0.5rem;

    background-color: var(--background-color);
    border-radius: 0.725rem;
    border: 2px solid var(--border-color);

    cursor: pointer;
    user-select: none;
`

export const CommandBoxIcon = styled.div`
    position: absolute;
    right: 1rem;

    display: flex;
    justify-content: center;
    align-items: center;
    width: 2.5rem;
    height: 2.5rem;

    background-color: var(--border-color);
    border-radius: 0.725rem;
`

export const CommandBoxCopy = styled(DocumentDuplicate)`
    width: 1.3rem;
    height: 1.3rem;

    color: var(--text-color);
    cursor: pointer;
`

export const CommandBoxCopied = styled(CheckCircle)`
    width: 1.2rem;
    height: 1.2rem;

    color: var(--secondary-color);
    border-radius: 0.725rem;
`
