import styled from 'styled-components'

export const LayoutWrapper = styled.div`
    display: grid;
    grid-template-rows: auto 1fr;
    height: 100vh;
    width: 100%;
    background: linear-gradient(180deg, #000 0%, #1d215a 100%);
`

export const LayoutContent = styled.div`
    display: flex;
    flex-direction: column;
    gap: 2rem;
    width: 100%;
    height: 100%;
    overflow-y: auto;
    padding: 2rem;

    @media screen and (max-width: 1024px) {
        padding: 3rem 1rem;
    }
`

export const SectionWrapper = styled.div`
    max-width: 1200px;
    margin: 0 auto;

    overflow-y: auto;
    height: 220vh;

    padding: 2rem;

    @media screen and (max-width: 1376px) {
        max-width: 80%;
    }

    @media screen and (max-width: 1024px) {
        padding: 1.5rem;
        max-width: 90%;
    }

    @media screen and (max-width: 768px) {
        padding: 1rem;
    }
`
