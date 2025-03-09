import styled from 'styled-components'
import { ButtonCSS } from '../index.styles'

export const CTABoxWrapper = styled.div`
    width: 100%;
    height: 100%;

    display: flex;
    flex-direction: column;
    gap: 3rem;
    justify-content: space-between;
`

export const CTABoxContent = styled.div`
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    user-select: none;

    @media (max-width: 768px) {
        gap: 3rem;
    }
`

export const CTAButton = styled.a<{ $left?: boolean }>`
    ${ButtonCSS}
    align-self: ${({ $left }) => ($left ? 'flex-start' : 'flex-end')};
`
