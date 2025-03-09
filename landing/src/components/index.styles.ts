import styled, { css } from 'styled-components'

export const HeroSection = styled.div`
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2rem;

    @media (max-width: 1024px) {
        padding: 1rem;
    }

    @media (max-width: 768px) {
        padding: 0.5rem;
    }
`

export const HeroContentWrapper = styled.div`
    max-width: 1200px;
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 3rem;

    @media (max-width: 1024px) {
        gap: 1.5rem;
        padding: 0 1rem;
    }

    @media (max-width: 768px) {
        gap: 1rem;
    }

    @media (max-width: 600px) {
        padding: 0 0.5rem;
    }
`

export const ButtonCSS = css`
    padding: 0.5rem 3rem;
    border: 1px solid #000;
    border-radius: 0.725rem;

    height: 3rem;
    min-width: 7.5rem;

    display: flex;
    justify-content: center;
    align-items: center;

    background-color: var(--primary-color);
    color: var(--text-color);
    font-size: 1rem;
    cursor: pointer;
    user-select: none;

    text-decoration: none;

    transition: background-color 0.2s ease-in-out, border 0.2s ease-in-out;

    &:hover {
        background-color: var(--background-color);
        border: 1px solid var(--primary-color);
        text-decoration: none;
    }

    @media screen and (max-width: 1024px) {
        width: 100%;
    }
`

export const Button = styled.button`
    ${ButtonCSS}
`

export const ButtonLink = styled.a`
    ${ButtonCSS}
`

export const HeroTitle = styled.h1`
    font-size: 3rem;
    line-height: 3.5rem;
    color: var(--text-color);

    @media screen and (max-width: 1024px) {
        font-size: 2.5rem;
        line-height: 3rem;
    }
`

export const HeroText = styled.p`
    font-size: 1rem;
    color: var(--text-color);
`

export const HeroList = styled.ul`
    display: flex;
    flex-direction: column;
    gap: 1rem;
    list-style-type: disc;
    padding-left: 2.5rem;

    @media screen and (max-width: 600px) {
        padding-left: 0.5rem;
    }
`

export const HeroListItem = styled.li`
    font-size: 1rem;
    color: var(--text-color);
`

export const ScenarioBox = styled.div`
    display: flex;
    flex-direction: column;

    width: 100%;
    height: 100%;

    gap: 1rem;
    padding: 3rem 2rem;

    background-color: var(--background-color);
    border-radius: 0.725rem;
    border: 2px solid var(--border-color);

    cursor: crosshair;
    user-select: none;
`

export const ScenarioItem = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: flex-start;

    gap: 1rem;
`

export const CodeParagraph = styled.p`
    font-size: 1.2rem;
    line-height: 1.5rem;
    color: var(--text-color);
`

export const PrimaryHighlight = styled.span`
    color: var(--primary-color);
`

export const SecondaryHighlight = styled.span`
    color: var(--secondary-color);
`

export const AccentHighlight = styled.span`
    color: var(--accent-color);
`

export const DullHighlight = styled.span`
    color: var(--dull-color);
`

export const MobileTrim = styled.span`
    @media screen and (max-width: 600px) {
        display: none;
    }
`
