class Tooltip extends HTMLElement {
    connectedCallback() {
        console.log("Tooltip::connectedCallback")
        this.setup()
    }

    handleDropdownPosition() {
        console.log("Tooltip::handleDropdownPosition")
        const screenPadding = 16

        const placeholderRect = this.placeholder.getBoundingClientRect()
        const dropdownRect = this.dropdown.getBoundingClientRect()

        // 相对于整个viewport的右端
        const dropdownRightX = dropdownRect.x + dropdownRect.width
        const placeholderRightX = placeholderRect.x + placeholderRect.width

        if (dropdownRect.x < 0) {
            // 左边超出viewport：设置左边距离viewport为screenPadding
            this.dropdown.style.left = '0'
            this.dropdown.style.right = 'auto'
            this.dropdown.style.transform = `translateX(${-placeholderRect.x + screenPadding}px)`
        } else if (dropdownRightX > window.innerWidth) {
            // 右边超出viewport：设置右边距离viewport为screenPadding
            // 注意innerWidth和outerWidth的区别
            this.dropdown.style.right = '0'
            this.dropdown.style.left = 'auto'
            this.dropdown.style.transform = `translateX(${window.innerWidth - placeholderRightX - screenPadding}px)`
        } else {
            // 正常显示
            this.dropdown.style.left = `-10%`
            this.dropdown.style.right = 'auto'
        }
    }

    toggle() {
        console.log("Tooltip::toggle")
        if (this.classList.contains('tooltip--open')) {
            this.close()
        } else {
            this.open()
        }
    }

    open() {
        console.log("Tooltip::open")
        this.classList.add('tooltip--open')
        this.handleDropdownPosition()
    }

    close() {
        console.log("Tooltip::close")
        this.classList.remove('tooltip--open')
    }

    setup() {
        console.log("Tooltip::setup")
        const ids = this.getAttribute("aria-describedby").split(' ')
        for (const i in ids) {
            const element = window.document.getElementById(ids[i])
            if (element === null) {
                continue
            }
            if (element.hasAttribute("data-tooltip-placeholder")) {
                this.placeholder = element
            } else if (element.hasAttribute("data-tooltip-dropdown")) {
                this.dropdown = element
            }
        }
        if (this.placeholder === undefined || this.placeholder === null) {
            this.placeholder = this.querySelector('[data-tooltip-placeholder]')
        } 
        if (this.dropdown === undefined || this.dropdown === null) {
            this.dropdown = this.querySelector('[data-tooltip-dropdown]')
        }

        // 不要使用mouseover
        this.placeholder.addEventListener('mouseenter', () => this.handleDropdownPosition())
        this.placeholder.addEventListener('touchstart', () => this.toggle())
    }
}

function dismissAllTooltips(event) {
    console.log("dismissAllTooltips")
    if (typeof event.target.closest !== 'function') return
    const currentTooltip = event.target.closest('carwow-tooltip')

    document.querySelectorAll('.tooltip--open').forEach((tooltip) => {
        if (tooltip === currentTooltip) return

        tooltip.classList.remove('tooltip--open')
    })
}

customElements.define('wow-tooltip', Tooltip)
document.addEventListener('touchstart', (e) => dismissAllTooltips(e))
