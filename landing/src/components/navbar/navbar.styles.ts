import { Bars3BottomRight, XMark } from '@styled-icons/heroicons-solid'
import { motion } from 'framer-motion'
import styled from 'styled-components'

export const NavbarWrapper = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;

    width: 100%;
    padding: 1.5rem 6rem;

    @media screen and (max-width: 1024px) {
        padding: 1rem 3rem;
    }

    @media screen and (max-width: 768px) {
        padding: 1rem 1.5rem;
    }
`

export const NavbarDesktop = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;

    width: 100%;
`

export const NavbarBackground = styled(motion.div)`
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;

    width: 100%;
    height: 100%;

    background-color: rgba(0, 0, 0, 0.5);

    z-index: 999;
`

export const NavbarMobile = styled(motion.div)`
    display: none;

    @media screen and (max-width: 1024px) {
        display: flex;
        flex-direction: column;
        gap: 2rem;

        justify-content: flex-start;
        align-items: start;

        position: fixed;

        top: 0;
        right: 0;
        bottom: 0;
        left: 0;

        width: 80%;
        height: 100%;

        background-color: var(--background-color);
        z-index: 1000;

        padding: 2rem;
    }
`

export const NavbarMobileHeader = styled.div`
    display: flex;
    justify-content: space-between;
    align-items: center;

    width: 100%;
`

export const NavbarMobileOpen = styled(Bars3BottomRight)`
    width: 2rem;
    height: 2rem;
    color: var(--text-color);

    cursor: pointer;

    @media screen and (min-width: 1024px) {
        display: none;
    }
`

export const NavbarMobileClose = styled(XMark)`
    width: 2rem;
    height: 2rem;
    color: var(--text-color);

    cursor: pointer;
`

export const NavbarLinks = styled.div<{ $mobileMenu?: boolean }>`
    display: ${({ $mobileMenu }) => ($mobileMenu ? 'none' : 'flex')};
    justify-content: space-between;
    align-items: center;

    width: ${({ $mobileMenu }) => ($mobileMenu ? '100%' : 'auto')};

    gap: 1rem;

    @media screen and (max-width: 1024px) {
        display: ${({ $mobileMenu }) => ($mobileMenu ? 'flex' : 'none')};

        height: 100%;

        flex-direction: column;
        justify-content: center;
        gap: 1rem;
    }
`

export const NavbarLogo = styled.img`
    height: 1.5rem;
    user-select: none;
    object-fit: contain;
`
