import { AnimatePresence, motion } from 'framer-motion'
import { useState } from 'react'

import helmInspect from '../../assets/logo/helm_inspect.svg'

import {
    NavbarBackground,
    NavbarDesktop,
    NavbarLinks,
    NavbarLogo,
    NavbarMobile,
    NavbarMobileClose,
    NavbarMobileHeader,
    NavbarMobileOpen,
    NavbarWrapper,
} from './navbar.styles'
import { ButtonLink } from '../index.styles'

const Navbar = () => {
    const [menuOpen, setMenuOpen] = useState(false)

    const toggleMenu = () => {
        setMenuOpen((prevState) => !prevState)
    }

    return (
        <NavbarWrapper>
            <NavbarDesktop>
                <NavbarLogo src={helmInspect} alt="Logo" />
                <NavbarLinks>
                    <ButtonLink
                        href="https://github.com/qreater/HelmInspect?tab=readme-ov-file#table-of-contents"
                        target="_blank"
                    >
                        Docs
                    </ButtonLink>
                    <ButtonLink
                        href="https://github.com/qreater"
                        target="_blank"
                    >
                        Qreater
                    </ButtonLink>
                </NavbarLinks>
                <NavbarMobileOpen onClick={toggleMenu} />
            </NavbarDesktop>

            <AnimatePresence>
                {menuOpen && (
                    <>
                        <NavbarBackground
                            as={motion.div}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.2 }}
                            onClick={toggleMenu}
                        />
                        <NavbarMobile
                            as={motion.div}
                            initial={{ x: '-100%', opacity: 0, scale: 0.9 }}
                            animate={{ x: 0, opacity: 1, scale: 1 }}
                            exit={{ x: '-100%', opacity: 0, scale: 0.95 }}
                            transition={{
                                duration: 0.3,
                                ease: [0.33, 1, 0.68, 1],
                            }}
                        >
                            <NavbarMobileHeader>
                                <NavbarLogo src={helmInspect} alt="Logo" />
                                <NavbarMobileClose onClick={toggleMenu} />
                            </NavbarMobileHeader>
                            <NavbarLinks $mobileMenu>
                                <ButtonLink
                                    href="https://github.com/qreater/HelmInspect?tab=readme-ov-file#table-of-contents"
                                    target="_blank"
                                >
                                    Docs
                                </ButtonLink>
                                <ButtonLink
                                    href="https://github.com/qreater"
                                    target="_blank"
                                >
                                    Qreater
                                </ButtonLink>
                            </NavbarLinks>
                        </NavbarMobile>
                    </>
                )}
            </AnimatePresence>
        </NavbarWrapper>
    )
}

export default Navbar
