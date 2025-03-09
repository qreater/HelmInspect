import styled from 'styled-components'

export const LandingContent = styled.div`
    width: 100%;
    max-width: 768px;
    margin-bottom: min(18vh, 30rem);
    height: 100%;
    align-self: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    gap: 3rem;
    text-align: center;
    user-select: none;

    @media (max-width: 768px) {
        margin-top: 5rem;
    }
`
