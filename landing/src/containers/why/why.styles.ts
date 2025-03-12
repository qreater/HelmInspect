import styled from 'styled-components'

export const WhyWrapper = styled.div`
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    justify-content: space-between;
    padding: 2rem;

    @media (max-width: 1024px) {
        padding: 0;
    }
`

export const WhyContent = styled.div`
    display: grid;
    gap: 2rem;
    grid-template-columns: 1fr 1fr;
    height: 100%;
    width: 100%;

    @media (max-width: 1024px) {
        display: flex;
        flex-direction: column;
    }
`
