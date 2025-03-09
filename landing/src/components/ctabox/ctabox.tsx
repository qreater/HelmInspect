import { CTABoxContent, CTABoxWrapper, CTAButton } from './ctabox.styles'

interface CTABoxProps {
    children: React.ReactNode
    CTAText: string
    CTALink: string
    CTANewTab?: boolean
    CTALeft?: boolean
}

export const CTABox = ({
    children,
    CTAText,
    CTALink,
    CTANewTab = false,
    CTALeft = false,
}: CTABoxProps) => {
    const directOrScroll = (
        e: React.MouseEvent<HTMLAnchorElement, MouseEvent>,
    ) => {
        if (CTALink.startsWith('#')) {
            e.preventDefault()
            document.getElementById(CTALink.slice(1))?.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
            })
        }
    }

    return (
        <CTABoxWrapper>
            <CTABoxContent>{children}</CTABoxContent>
            <CTAButton
                href={CTALink}
                target={CTANewTab ? '_blank' : undefined}
                onClick={directOrScroll}
                $left={CTALeft}
            >
                {CTAText}
            </CTAButton>
        </CTABoxWrapper>
    )
}
