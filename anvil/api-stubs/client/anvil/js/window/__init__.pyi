# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# DOM declarations adapted from webtypy - https://github.com/pyodide/webtypy
# Maintained here; generate the client stubs with doc/anvil-api-stubs/generate-stubs.mjs
#
"""The anvil.js.window module provides access to the browser's window object.

In Anvil, `window` is registered in `sys.modules` as `anvil.js.window`, allowing:

    from anvil.js.window import document
    from anvil.js.window import location
    from anvil.js.window import HTMLDivElement

This module exports all window properties as module-level attributes for convenient access.
DOM types are also available for type annotations.

[Anvil Docs](https://anvil.works/docs/client/javascript)

Generated from WebIDL specifications via webtypy.
"""

from typing import Any, Callable, Sequence, overload

class EventTarget:
    def addEventListener(self, type: str, callback: EventListener | None, options: AddEventListenerOptions | bool | None = {}) -> None: ...
    def removeEventListener(self, type: str, callback: EventListener | None, options: EventListenerOptions | bool | None = {}) -> None: ...
    def dispatchEvent(self, event: Event) -> bool: ...

class Event:
    type: str
    target: EventTarget | None
    srcElement: EventTarget | None
    currentTarget: EventTarget | None
    def composedPath(self) -> Sequence[EventTarget]: ...
    NONE = 0
    CAPTURING_PHASE = 1
    AT_TARGET = 2
    BUBBLING_PHASE = 3
    eventPhase: int
    def stopPropagation(self) -> None: ...
    cancelBubble: bool
    def stopImmediatePropagation(self) -> None: ...
    bubbles: bool
    cancelable: bool
    returnValue: bool
    def preventDefault(self) -> None: ...
    defaultPrevented: bool
    composed: bool
    isTrusted: bool
    timeStamp: DOMHighResTimeStamp
    def initEvent(self, type: str, bubbles: bool | None = False, cancelable: bool | None = False) -> None: ...

class UIEvent(Event):
    sourceCapabilities: InputDeviceCapabilities | None
    view: Window | None
    detail: int
    def initUIEvent(self, typeArg: str, bubblesArg: bool | None = False, cancelableArg: bool | None = False, viewArg: Window | None = None, detailArg: int | None = 0) -> None: ...
    which: int

class MouseEvent(UIEvent):
    pageX: float
    pageY: float
    x: float
    y: float
    offsetX: float
    offsetY: float
    movementX: float
    movementY: float
    screenX: int
    screenY: int
    clientX: int
    clientY: int
    ctrlKey: bool
    shiftKey: bool
    altKey: bool
    metaKey: bool
    button: short
    buttons: int
    relatedTarget: EventTarget | None
    def getModifierState(self, keyArg: str) -> bool: ...
    def initMouseEvent(self, typeArg: str, bubblesArg: bool | None = False, cancelableArg: bool | None = False, viewArg: Window | None = None, detailArg: int | None = 0, screenXArg: int | None = 0, screenYArg: int | None = 0, clientXArg: int | None = 0, clientYArg: int | None = 0, ctrlKeyArg: bool | None = False, altKeyArg: bool | None = False, shiftKeyArg: bool | None = False, metaKeyArg: bool | None = False, buttonArg: short | None = 0, relatedTargetArg: EventTarget | None = None) -> None: ...

class KeyboardEvent(UIEvent):
    DOM_KEY_LOCATION_STANDARD = 0x00
    DOM_KEY_LOCATION_LEFT = 0x01
    DOM_KEY_LOCATION_RIGHT = 0x02
    DOM_KEY_LOCATION_NUMPAD = 0x03
    key: str
    code: str
    location: int
    ctrlKey: bool
    shiftKey: bool
    altKey: bool
    metaKey: bool
    repeat: bool
    isComposing: bool
    def getModifierState(self, keyArg: str) -> bool: ...
    def initKeyboardEvent(self, typeArg: str, bubblesArg: bool | None = False, cancelableArg: bool | None = False, viewArg: Window | None = None, keyArg: str | None = "", locationArg: int | None = 0, ctrlKey: bool | None = False, altKey: bool | None = False, shiftKey: bool | None = False, metaKey: bool | None = False) -> None: ...
    charCode: int
    keyCode: int

class FocusEvent(UIEvent):
    relatedTarget: EventTarget | None

class InputEvent(UIEvent):
    dataTransfer: DataTransfer | None
    def getTargetRanges(self) -> Sequence[StaticRange]: ...
    data: str | None
    isComposing: bool
    inputType: str

class WheelEvent(MouseEvent):
    DOM_DELTA_PIXEL = 0x00
    DOM_DELTA_LINE = 0x01
    DOM_DELTA_PAGE = 0x02
    deltaX: float
    deltaY: float
    deltaZ: float
    deltaMode: int

class TouchEvent(UIEvent):
    touches: TouchList
    targetTouches: TouchList
    changedTouches: TouchList
    altKey: bool
    metaKey: bool
    ctrlKey: bool
    shiftKey: bool

class Touch:
    identifier: int
    target: EventTarget
    screenX: float
    screenY: float
    clientX: float
    clientY: float
    pageX: float
    pageY: float
    radiusX: float
    radiusY: float
    rotationAngle: float
    force: float
    altitudeAngle: float
    azimuthAngle: float
    touchType: TouchType

class TouchList:
    length: int

class PointerEvent(MouseEvent):
    pointerId: int
    width: float
    height: float
    pressure: float
    tangentialPressure: float
    tiltX: int
    tiltY: int
    twist: int
    altitudeAngle: float
    azimuthAngle: float
    pointerType: str
    isPrimary: bool
    def getCoalescedEvents(self) -> Sequence[PointerEvent]: ...
    def getPredictedEvents(self) -> Sequence[PointerEvent]: ...

class DragEvent(MouseEvent):
    dataTransfer: DataTransfer | None

class ClipboardEvent(Event):
    clipboardData: DataTransfer | None

class AnimationEvent(Event):
    animationName: CSSOMString
    elapsedTime: float
    pseudoElement: CSSOMString

class TransitionEvent(Event):
    propertyName: CSSOMString
    elapsedTime: float
    pseudoElement: CSSOMString

class CustomEvent(Event):
    detail: Any
    def initCustomEvent(self, type: str, bubbles: bool | None = False, cancelable: bool | None = False, detail: Any | None = None) -> None: ...

class ErrorEvent(Event):
    message: str
    filename: USVString
    lineno: int
    colno: int
    error: Any

class ProgressEvent(Event):
    lengthComputable: bool
    loaded: int
    total: int

class SubmitEvent(Event):
    submitter: HTMLElement | None

class FormDataEvent(Event):
    formData: FormData

class HashChangeEvent(Event):
    oldURL: USVString
    newURL: USVString

class PopStateEvent(Event):
    state: Any

class StorageEvent(Event):
    key: str | None
    oldValue: str | None
    newValue: str | None
    url: USVString
    storageArea: Storage | None
    def initStorageEvent(self, type: str, bubbles: bool | None = False, cancelable: bool | None = False, key: str | None = None, oldValue: str | None = None, newValue: str | None = None, url: USVString | None = "", storageArea: Storage | None = None) -> None: ...

class MessageEvent(Event):
    data: Any
    origin: USVString
    lastEventId: str
    source: MessageEventSource | None
    ports: Sequence[MessagePort]
    def initMessageEvent(self, type: str, bubbles: bool | None = False, cancelable: bool | None = False, data: Any | None = None, origin: USVString | None = "", lastEventId: str | None = "", source: MessageEventSource | None = None, ports: Sequence[MessagePort] | None = []) -> None: ...

class BeforeUnloadEvent(Event):
    returnValue: str

class Node(EventTarget):
    ELEMENT_NODE = 1
    ATTRIBUTE_NODE = 2
    TEXT_NODE = 3
    CDATA_SECTION_NODE = 4
    ENTITY_REFERENCE_NODE = 5
    ENTITY_NODE = 6
    PROCESSING_INSTRUCTION_NODE = 7
    COMMENT_NODE = 8
    DOCUMENT_NODE = 9
    DOCUMENT_TYPE_NODE = 10
    DOCUMENT_FRAGMENT_NODE = 11
    NOTATION_NODE = 12
    nodeType: int
    nodeName: str
    baseURI: USVString
    isConnected: bool
    ownerDocument: Document | None
    def getRootNode(self, options: GetRootNodeOptions | None = {}) -> Node: ...
    parentNode: Node | None
    parentElement: Element | None
    def hasChildNodes(self) -> bool: ...
    childNodes: NodeList
    firstChild: Node | None
    lastChild: Node | None
    previousSibling: Node | None
    nextSibling: Node | None
    nodeValue: str | None
    textContent: str | None
    def normalize(self) -> None: ...
    def cloneNode(self, deep: bool | None = False) -> Node: ...
    def isEqualNode(self, otherNode: Node | None) -> bool: ...
    def isSameNode(self, otherNode: Node | None) -> bool: ...
    DOCUMENT_POSITION_DISCONNECTED = 0x01
    DOCUMENT_POSITION_PRECEDING = 0x02
    DOCUMENT_POSITION_FOLLOWING = 0x04
    DOCUMENT_POSITION_CONTAINS = 0x08
    DOCUMENT_POSITION_CONTAINED_BY = 0x10
    DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC = 0x20
    def compareDocumentPosition(self, other: Node) -> int: ...
    def contains(self, other: Node | None) -> bool: ...
    def lookupPrefix(self, namespace: str | None) -> str | None: ...
    def lookupNamespaceURI(self, prefix: str | None) -> str | None: ...
    def isDefaultNamespace(self, namespace: str | None) -> bool: ...
    def insertBefore(self, node: Node, child: Node | None) -> Node: ...
    def appendChild(self, node: Node) -> Node: ...
    def replaceChild(self, node: Node, child: Node) -> Node: ...
    def removeChild(self, child: Node) -> Node: ...

class NodeList:
    length: int

class Element(Node, InnerHTML, Region, GeometryUtils, ParentNode, NonDocumentTypeChildNode, ChildNode, Slottable, ARIAMixin, Animatable):
    textContent: str
    outerHTML: str
    def insertAdjacentHTML(self, position: str, text: str) -> None: ...
    def getSpatialNavigationContainer(self) -> Node: ...
    def focusableAreas(self, option: FocusableAreasOption | None = {}) -> Sequence[Node]: ...
    def spatialNavigationSearch(self, dir: SpatialNavigationDirection, options: SpatialNavigationSearchOptions | None = {}) -> Node | None: ...
    def pseudo(self, type: CSSOMString) -> CSSPseudoElement | None: ...
    part: DOMTokenList
    def computedStyleMap(self) -> StylePropertyMapReadOnly: ...
    def getClientRects(self) -> DOMRectList: ...
    def getBoundingClientRect(self) -> DOMRect: ...
    def checkVisibility(self, options: CheckVisibilityOptions | None = {}) -> bool: ...
    def scrollIntoView(self, arg: bool | ScrollIntoViewOptions | None = {}) -> None: ...
    @overload
    def scroll(self, options: ScrollToOptions | None = {}) -> None: ...
    @overload
    def scroll(self, x: float, y: float) -> None: ...
    @overload
    def scrollTo(self, options: ScrollToOptions | None = {}) -> None: ...
    @overload
    def scrollTo(self, x: float, y: float) -> None: ...
    @overload
    def scrollBy(self, options: ScrollToOptions | None = {}) -> None: ...
    @overload
    def scrollBy(self, x: float, y: float) -> None: ...
    scrollTop: float
    scrollLeft: float
    scrollWidth: int
    scrollHeight: int
    clientTop: int
    clientLeft: int
    clientWidth: int
    clientHeight: int
    namespaceURI: str | None
    prefix: str | None
    localName: str
    tagName: str
    id: str
    className: str
    classList: DOMTokenList
    slot: str
    def hasAttributes(self) -> bool: ...
    attributes: NamedNodeMap
    def getAttributeNames(self) -> Sequence[str]: ...
    def getAttribute(self, qualifiedName: str) -> str | None: ...
    def getAttributeNS(self, namespace: str | None, localName: str) -> str | None: ...
    def setAttribute(self, qualifiedName: str, value: str) -> None: ...
    def setAttributeNS(self, namespace: str | None, qualifiedName: str, value: str) -> None: ...
    def removeAttribute(self, qualifiedName: str) -> None: ...
    def removeAttributeNS(self, namespace: str | None, localName: str) -> None: ...
    def toggleAttribute(self, qualifiedName: str, force: bool | None = None) -> bool: ...
    def hasAttribute(self, qualifiedName: str) -> bool: ...
    def hasAttributeNS(self, namespace: str | None, localName: str) -> bool: ...
    def getAttributeNode(self, qualifiedName: str) -> Attr | None: ...
    def getAttributeNodeNS(self, namespace: str | None, localName: str) -> Attr | None: ...
    def setAttributeNode(self, attr: Attr) -> Attr | None: ...
    def setAttributeNodeNS(self, attr: Attr) -> Attr | None: ...
    def removeAttributeNode(self, attr: Attr) -> Attr: ...
    def attachShadow(self, init: ShadowRootInit) -> ShadowRoot: ...
    shadowRoot: ShadowRoot | None
    def closest(self, selectors: str) -> Element | None: ...
    def matches(self, selectors: str) -> bool: ...
    def webkitMatchesSelector(self, selectors: str) -> bool: ...
    def getElementsByTagName(self, qualifiedName: str) -> HTMLCollection: ...
    def getElementsByTagNameNS(self, namespace: str | None, localName: str) -> HTMLCollection: ...
    def getElementsByClassName(self, classNames: str) -> HTMLCollection: ...
    def insertAdjacentElement(self, where: str, element: Element) -> Element | None: ...
    def insertAdjacentText(self, where: str, data: str) -> None: ...
    editContext: EditContext | None
    elementTiming: str
    def requestFullscreen(self, options: FullscreenOptions | None = {}) -> None: ...
    onfullscreenchange: EventHandler
    onfullscreenerror: EventHandler
    def setPointerCapture(self, pointerId: int) -> None: ...
    def releasePointerCapture(self, pointerId: int) -> None: ...
    def hasPointerCapture(self, pointerId: int) -> bool: ...
    def requestPointerLock(self) -> None: ...
    def setHTML(self, input: str, options: SetHTMLOptions | None = {}) -> None: ...

class HTMLCollection:
    length: int

class DOMTokenList:
    length: int
    def contains(self, token: str) -> bool: ...
    def add(self, *tokens: str) -> None: ...
    def remove(self, *tokens: str) -> None: ...
    def toggle(self, token: str, force: bool | None = None) -> bool: ...
    def replace(self, token: str, newToken: str) -> bool: ...
    def supports(self, token: str) -> bool: ...
    value: str

class DOMRect(DOMRectReadOnly):
    x: float
    y: float
    width: float
    height: float

class DOMRectReadOnly:
    x: float
    y: float
    width: float
    height: float
    top: float
    right: float
    bottom: float
    left: float
    def toJSON(self) -> object: ...

class InnerHTML:
    innerHTML: str

class Region:
    regionOverset: CSSOMString
    def getRegionFlowRanges(self) -> Sequence[Range]: ...

class GeometryUtils:
    def getBoxQuads(self, options: BoxQuadOptions | None = {}) -> Sequence[DOMQuad]: ...
    def convertQuadFromNode(self, quad: DOMQuadInit, from_: GeometryNode, options: ConvertCoordinateOptions | None = {}) -> DOMQuad: ...
    def convertRectFromNode(self, rect: DOMRectReadOnly, from_: GeometryNode, options: ConvertCoordinateOptions | None = {}) -> DOMQuad: ...
    def convertPointFromNode(self, point: DOMPointInit, from_: GeometryNode, options: ConvertCoordinateOptions | None = {}) -> DOMPoint: ...

class NonDocumentTypeChildNode:
    previousElementSibling: Element | None
    nextElementSibling: Element | None

class ARIAMixin:
    role: str | None
    ariaActiveDescendantElement: Element | None
    ariaAtomic: str | None
    ariaAutoComplete: str | None
    ariaBusy: str | None
    ariaChecked: str | None
    ariaColCount: str | None
    ariaColIndex: str | None
    ariaColIndexText: str | None
    ariaColSpan: str | None
    ariaControlsElements: Sequence[Element]
    ariaCurrent: str | None
    ariaDescribedByElements: Sequence[Element]
    ariaDescription: str | None
    ariaDetailsElements: Sequence[Element]
    ariaDisabled: str | None
    ariaErrorMessageElements: Sequence[Element]
    ariaExpanded: str | None
    ariaFlowToElements: Sequence[Element]
    ariaHasPopup: str | None
    ariaHidden: str | None
    ariaInvalid: str | None
    ariaKeyShortcuts: str | None
    ariaLabel: str | None
    ariaLabelledByElements: Sequence[Element]
    ariaLevel: str | None
    ariaLive: str | None
    ariaModal: str | None
    ariaMultiLine: str | None
    ariaMultiSelectable: str | None
    ariaOrientation: str | None
    ariaOwnsElements: Sequence[Element]
    ariaPlaceholder: str | None
    ariaPosInSet: str | None
    ariaPressed: str | None
    ariaReadOnly: str | None
    ariaRequired: str | None
    ariaRoleDescription: str | None
    ariaRowCount: str | None
    ariaRowIndex: str | None
    ariaRowIndexText: str | None
    ariaRowSpan: str | None
    ariaSelected: str | None
    ariaSetSize: str | None
    ariaSort: str | None
    ariaValueMax: str | None
    ariaValueMin: str | None
    ariaValueNow: str | None
    ariaValueText: str | None

class Animatable:
    def animate(self, keyframes: object | None, options: float | KeyframeAnimationOptions | None = {}) -> Animation: ...
    def getAnimations(self, options: GetAnimationsOptions | None = {}) -> Sequence[Animation]: ...

class ElementCSSInlineStyle:
    attributeStyleMap: StylePropertyMap
    style: CSSStyleDeclaration

class ElementContentEditable:
    contentEditable: str
    enterKeyHint: str
    isContentEditable: bool
    inputMode: str
    virtualKeyboardPolicy: str

class HTMLOrSVGElement:
    dataset: DOMStringMap
    nonce: str
    autofocus: bool
    tabIndex: int
    def focus(self, options: FocusOptions | None = {}) -> None: ...
    def blur(self) -> None: ...

class NonElementParentNode:
    def getElementById(self, elementId: str) -> Element | None: ...

class ParentNode:
    children: HTMLCollection
    firstElementChild: Element | None
    lastElementChild: Element | None
    childElementCount: int
    def prepend(self, *nodes: Node | str) -> None: ...
    def append(self, *nodes: Node | str) -> None: ...
    def replaceChildren(self, *nodes: Node | str) -> None: ...
    def querySelector(self, selectors: str) -> Element | None: ...
    def querySelectorAll(self, selectors: str) -> NodeList: ...

class ChildNode:
    def before(self, *nodes: Node | str) -> None: ...
    def after(self, *nodes: Node | str) -> None: ...
    def replaceWith(self, *nodes: Node | str) -> None: ...
    def remove(self) -> None: ...

class Slottable:
    assignedSlot: HTMLSlotElement | None

class DocumentOrShadowRoot:
    styleSheets: StyleSheetList
    adoptedStyleSheets: Sequence[CSSStyleSheet]
    fullscreenElement: Element | None
    activeElement: Element | None
    pictureInPictureElement: Element | None
    pointerLockElement: Element | None
    def getAnimations(self) -> Sequence[Animation]: ...

class GlobalEventHandlers:
    onanimationstart: EventHandler
    onanimationiteration: EventHandler
    onanimationend: EventHandler
    onanimationcancel: EventHandler
    ontransitionrun: EventHandler
    ontransitionstart: EventHandler
    ontransitionend: EventHandler
    ontransitioncancel: EventHandler
    onabort: EventHandler
    onauxclick: EventHandler
    onbeforeinput: EventHandler
    onbeforematch: EventHandler
    onblur: EventHandler
    oncancel: EventHandler
    oncanplay: EventHandler
    oncanplaythrough: EventHandler
    onchange: EventHandler
    onclick: EventHandler
    onclose: EventHandler
    oncontextlost: EventHandler
    oncontextmenu: EventHandler
    oncontextrestored: EventHandler
    oncopy: EventHandler
    oncuechange: EventHandler
    oncut: EventHandler
    ondblclick: EventHandler
    ondrag: EventHandler
    ondragend: EventHandler
    ondragenter: EventHandler
    ondragleave: EventHandler
    ondragover: EventHandler
    ondragstart: EventHandler
    ondrop: EventHandler
    ondurationchange: EventHandler
    onemptied: EventHandler
    onended: EventHandler
    onerror: OnErrorEventHandler
    onfocus: EventHandler
    onformdata: EventHandler
    oninput: EventHandler
    oninvalid: EventHandler
    onkeydown: EventHandler
    onkeypress: EventHandler
    onkeyup: EventHandler
    onload: EventHandler
    onloadeddata: EventHandler
    onloadedmetadata: EventHandler
    onloadstart: EventHandler
    onmousedown: EventHandler
    onmouseenter: EventHandler
    onmouseleave: EventHandler
    onmousemove: EventHandler
    onmouseout: EventHandler
    onmouseover: EventHandler
    onmouseup: EventHandler
    onpaste: EventHandler
    onpause: EventHandler
    onplay: EventHandler
    onplaying: EventHandler
    onprogress: EventHandler
    onratechange: EventHandler
    onreset: EventHandler
    onresize: EventHandler
    onscroll: EventHandler
    onscrollend: EventHandler
    onsecuritypolicyviolation: EventHandler
    onseeked: EventHandler
    onseeking: EventHandler
    onselect: EventHandler
    onslotchange: EventHandler
    onstalled: EventHandler
    onsubmit: EventHandler
    onsuspend: EventHandler
    ontimeupdate: EventHandler
    ontoggle: EventHandler
    onvolumechange: EventHandler
    onwaiting: EventHandler
    onwebkitanimationend: EventHandler
    onwebkitanimationiteration: EventHandler
    onwebkitanimationstart: EventHandler
    onwebkittransitionend: EventHandler
    onwheel: EventHandler
    onpointerover: EventHandler
    onpointerenter: EventHandler
    onpointerdown: EventHandler
    onpointermove: EventHandler
    onpointerrawupdate: EventHandler
    onpointerup: EventHandler
    onpointercancel: EventHandler
    onpointerout: EventHandler
    onpointerleave: EventHandler
    ongotpointercapture: EventHandler
    onlostpointercapture: EventHandler
    onselectstart: EventHandler
    onselectionchange: EventHandler
    ontouchstart: EventHandler
    ontouchend: EventHandler
    ontouchmove: EventHandler
    ontouchcancel: EventHandler
    onbeforexrselect: EventHandler

class FontFaceSource:
    fonts: FontFaceSet

class XPathEvaluatorBase:
    def createExpression(self, expression: str, resolver: XPathNSResolver | None = None) -> XPathExpression: ...
    def createNSResolver(self, nodeResolver: Node) -> XPathNSResolver: ...
    def evaluate(self, expression: str, contextNode: Node, resolver: XPathNSResolver | None = None, type: int | None = 0, result: XPathResult | None = None) -> XPathResult: ...

class Document(Node, FontFaceSource, GeometryUtils, NonElementParentNode, DocumentOrShadowRoot, ParentNode, XPathEvaluatorBase, GlobalEventHandlers):
    rootElement: SVGSVGElement | None
    namedFlows: NamedFlowMap
    def startViewTransition(self, callback: UpdateCallback | None = None) -> ViewTransition: ...
    def elementFromPoint(self, x: float, y: float) -> Element | None: ...
    def elementsFromPoint(self, x: float, y: float) -> Sequence[Element]: ...
    def caretPositionFromPoint(self, x: float, y: float) -> CaretPosition | None: ...
    scrollingElement: Element | None
    implementation: DOMImplementation
    URL: USVString
    documentURI: USVString
    compatMode: str
    characterSet: str
    charset: str
    inputEncoding: str
    contentType: str
    doctype: DocumentType | None
    documentElement: Element | None
    def getElementsByTagName(self, qualifiedName: str) -> HTMLCollection: ...
    def getElementsByTagNameNS(self, namespace: str | None, localName: str) -> HTMLCollection: ...
    def getElementsByClassName(self, classNames: str) -> HTMLCollection: ...
    def createElement(self, localName: str, options: str | ElementCreationOptions | None = {}) -> Element: ...
    def createElementNS(self, namespace: str | None, qualifiedName: str, options: str | ElementCreationOptions | None = {}) -> Element: ...
    def createDocumentFragment(self) -> DocumentFragment: ...
    def createTextNode(self, data: str) -> Text: ...
    def createCDATASection(self, data: str) -> CDATASection: ...
    def createComment(self, data: str) -> Comment: ...
    def createProcessingInstruction(self, target: str, data: str) -> ProcessingInstruction: ...
    def importNode(self, node: Node, deep: bool | None = False) -> Node: ...
    def adoptNode(self, node: Node) -> Node: ...
    def createAttribute(self, localName: str) -> Attr: ...
    def createAttributeNS(self, namespace: str | None, qualifiedName: str) -> Attr: ...
    def createEvent(self, interface: str) -> Event: ...
    def createRange(self) -> Range: ...
    def createNodeIterator(self, root: Node, whatToShow: int | None = 0xFFFFFFFF, filter: NodeFilter | None = None) -> NodeIterator: ...
    def createTreeWalker(self, root: Node, whatToShow: int | None = 0xFFFFFFFF, filter: NodeFilter | None = None) -> TreeWalker: ...
    def measureElement(self, element: Element) -> FontMetrics: ...
    def measureText(self, text: str, styleMap: StylePropertyMapReadOnly) -> FontMetrics: ...
    fullscreenEnabled: bool
    fullscreen: bool
    def exitFullscreen(self) -> None: ...
    onfullscreenchange: EventHandler
    onfullscreenerror: EventHandler
    location: Location | None
    domain: USVString
    referrer: USVString
    cookie: USVString
    lastModified: str
    readyState: DocumentReadyState
    title: str
    dir: str
    body: HTMLElement | None
    head: HTMLHeadElement | None
    images: HTMLCollection
    embeds: HTMLCollection
    plugins: HTMLCollection
    links: HTMLCollection
    forms: HTMLCollection
    scripts: HTMLCollection
    def getElementsByName(self, elementName: str) -> NodeList: ...
    currentScript: HTMLOrSVGScriptElement | None
    @overload
    def open(self, unused1: str | None = None, unused2: str | None = None) -> Document: ...
    @overload
    def open(self, url: USVString, name: str, features: str) -> WindowProxy | None: ...
    def close(self) -> None: ...
    def write(self, *text: str) -> None: ...
    def writeln(self, *text: str) -> None: ...
    defaultView: WindowProxy | None
    def hasFocus(self) -> bool: ...
    designMode: str
    def execCommand(self, commandId: str, showUI: bool | None = False, value: str | None = "") -> bool: ...
    def queryCommandEnabled(self, commandId: str) -> bool: ...
    def queryCommandIndeterm(self, commandId: str) -> bool: ...
    def queryCommandState(self, commandId: str) -> bool: ...
    def queryCommandSupported(self, commandId: str) -> bool: ...
    def queryCommandValue(self, commandId: str) -> str: ...
    hidden: bool
    visibilityState: DocumentVisibilityState
    onreadystatechange: EventHandler
    onvisibilitychange: EventHandler
    fgColor: str
    linkColor: str
    vlinkColor: str
    alinkColor: str
    bgColor: str
    anchors: HTMLCollection
    applets: HTMLCollection
    def clear(self) -> None: ...
    def captureEvents(self) -> None: ...
    def releaseEvents(self) -> None: ...
    all: HTMLAllCollection
    onfreeze: EventHandler
    onresume: EventHandler
    wasDiscarded: bool
    permissionsPolicy: PermissionsPolicy
    pictureInPictureEnabled: bool
    def exitPictureInPicture(self) -> None: ...
    onpointerlockchange: EventHandler
    onpointerlockerror: EventHandler
    def exitPointerLock(self) -> None: ...
    prerendering: bool
    onprerenderingchange: EventHandler
    fragmentDirective: FragmentDirective
    def getSelection(self) -> Selection | None: ...
    def hasStorageAccess(self) -> bool: ...
    def requestStorageAccess(self) -> None: ...
    timeline: DocumentTimeline

class DocumentFragment(Node, NonElementParentNode, ParentNode):
    ...
    ...

class HTMLElement(Element, ElementCSSInlineStyle, GlobalEventHandlers, ElementContentEditable, HTMLOrSVGElement):
    offsetParent: Element | None
    offsetTop: int
    offsetLeft: int
    offsetWidth: int
    offsetHeight: int
    title: str
    lang: str
    translate: bool
    dir: str
    hidden: bool | float | str | None
    inert: bool
    def click(self) -> None: ...
    accessKey: str
    accessKeyLabel: str
    draggable: bool
    spellcheck: bool
    autocapitalize: str
    innerText: str
    outerText: str
    def attachInternals(self) -> ElementInternals: ...

class HTMLDivElement(HTMLElement):
    align: str

class HTMLSpanElement(HTMLElement):
    ...
    ...

class HTMLParagraphElement(HTMLElement):
    align: str

class HTMLHeadingElement(HTMLElement):
    align: str

class HTMLBRElement(HTMLElement):
    clear: str

class HTMLHRElement(HTMLElement):
    align: str
    color: str
    noShade: bool
    size: str
    width: str

class HTMLPreElement(HTMLElement):
    width: int

class HTMLQuoteElement(HTMLElement):
    cite: USVString

class HTMLLabelElement(HTMLElement):
    form: HTMLFormElement | None
    htmlFor: str
    control: HTMLElement | None

class HTMLLIElement(HTMLElement):
    value: int
    type: str

class HTMLUListElement(HTMLElement):
    compact: bool
    type: str

class HTMLOListElement(HTMLElement):
    reversed: bool
    start: int
    type: str
    compact: bool

class HTMLTableElement(HTMLElement):
    caption: HTMLTableCaptionElement | None
    def createCaption(self) -> HTMLTableCaptionElement: ...
    def deleteCaption(self) -> None: ...
    tHead: HTMLTableSectionElement | None
    def createTHead(self) -> HTMLTableSectionElement: ...
    def deleteTHead(self) -> None: ...
    tFoot: HTMLTableSectionElement | None
    def createTFoot(self) -> HTMLTableSectionElement: ...
    def deleteTFoot(self) -> None: ...
    tBodies: HTMLCollection
    def createTBody(self) -> HTMLTableSectionElement: ...
    rows: HTMLCollection
    def insertRow(self, index: int | None = -1) -> HTMLTableRowElement: ...
    def deleteRow(self, index: int) -> None: ...
    align: str
    border: str
    frame: str
    rules: str
    summary: str
    width: str
    bgColor: str
    cellPadding: str
    cellSpacing: str

class HTMLTableRowElement(HTMLElement):
    rowIndex: int
    sectionRowIndex: int
    cells: HTMLCollection
    def insertCell(self, index: int | None = -1) -> HTMLTableCellElement: ...
    def deleteCell(self, index: int) -> None: ...
    align: str
    ch: str
    chOff: str
    vAlign: str
    bgColor: str

class HTMLTableCellElement(HTMLElement):
    colSpan: int
    rowSpan: int
    headers: str
    cellIndex: int
    scope: str
    abbr: str
    align: str
    axis: str
    height: str
    width: str
    ch: str
    chOff: str
    noWrap: bool
    vAlign: str
    bgColor: str

class HTMLTableSectionElement(HTMLElement):
    rows: HTMLCollection
    def insertRow(self, index: int | None = -1) -> HTMLTableRowElement: ...
    def deleteRow(self, index: int) -> None: ...
    align: str
    ch: str
    chOff: str
    vAlign: str

class HTMLFormElement(HTMLElement):
    acceptCharset: str
    action: USVString
    autocomplete: str
    enctype: str
    encoding: str
    method: str
    name: str
    noValidate: bool
    target: str
    rel: str
    relList: DOMTokenList
    elements: HTMLFormControlsCollection
    length: int
    def submit(self) -> None: ...
    def requestSubmit(self, submitter: HTMLElement | None = None) -> None: ...
    def reset(self) -> None: ...
    def checkValidity(self) -> bool: ...
    def reportValidity(self) -> bool: ...

class HTMLInputElement(HTMLElement):
    webkitdirectory: bool
    webkitEntries: Sequence[FileSystemEntry]
    capture: str
    accept: str
    alt: str
    autocomplete: str
    defaultChecked: bool
    checked: bool
    dirName: str
    disabled: bool
    form: HTMLFormElement | None
    files: FileList | None
    formAction: USVString
    formEnctype: str
    formMethod: str
    formNoValidate: bool
    formTarget: str
    height: int
    indeterminate: bool
    list: HTMLDataListElement | None
    max: str
    maxLength: int
    min: str
    minLength: int
    multiple: bool
    name: str
    pattern: str
    placeholder: str
    readOnly: bool
    required: bool
    size: int
    src: USVString
    step: str
    type: str
    defaultValue: str
    value: str
    valueAsDate: object | None
    valueAsNumber: float
    width: int
    def stepUp(self, n: int | None = 1) -> None: ...
    def stepDown(self, n: int | None = 1) -> None: ...
    willValidate: bool
    validity: ValidityState
    validationMessage: str
    def checkValidity(self) -> bool: ...
    def reportValidity(self) -> bool: ...
    def setCustomValidity(self, error: str) -> None: ...
    labels: NodeList | None
    def select(self) -> None: ...
    selectionStart: int | None
    selectionEnd: int | None
    selectionDirection: str | None
    @overload
    def setRangeText(self, replacement: str) -> None: ...
    @overload
    def setRangeText(self, replacement: str, start: int, end: int, selectionMode: SelectionMode | None = "preserve") -> None: ...
    def setSelectionRange(self, start: int, end: int, direction: str | None = None) -> None: ...
    def showPicker(self) -> None: ...
    align: str
    useMap: str

class HTMLTextAreaElement(HTMLElement):
    autocomplete: str
    cols: int
    dirName: str
    disabled: bool
    form: HTMLFormElement | None
    maxLength: int
    minLength: int
    name: str
    placeholder: str
    readOnly: bool
    required: bool
    rows: int
    wrap: str
    type: str
    defaultValue: str
    value: str
    textLength: int
    willValidate: bool
    validity: ValidityState
    validationMessage: str
    def checkValidity(self) -> bool: ...
    def reportValidity(self) -> bool: ...
    def setCustomValidity(self, error: str) -> None: ...
    labels: NodeList
    def select(self) -> None: ...
    selectionStart: int
    selectionEnd: int
    selectionDirection: str
    @overload
    def setRangeText(self, replacement: str) -> None: ...
    @overload
    def setRangeText(self, replacement: str, start: int, end: int, selectionMode: SelectionMode | None = "preserve") -> None: ...
    def setSelectionRange(self, start: int, end: int, direction: str | None = None) -> None: ...

class HTMLSelectElement(HTMLElement):
    autocomplete: str
    disabled: bool
    form: HTMLFormElement | None
    multiple: bool
    name: str
    required: bool
    size: int
    type: str
    options: HTMLOptionsCollection
    length: int
    def namedItem(self, name: str) -> HTMLOptionElement | None: ...
    def add(self, element: HTMLOptionElement | HTMLOptGroupElement, before: HTMLElement | int | None = None) -> None: ...
    @overload
    def remove(self) -> None: ...
    @overload
    def remove(self, index: int) -> None: ...
    selectedOptions: HTMLCollection
    selectedIndex: int
    value: str
    willValidate: bool
    validity: ValidityState
    validationMessage: str
    def checkValidity(self) -> bool: ...
    def reportValidity(self) -> bool: ...
    def setCustomValidity(self, error: str) -> None: ...
    labels: NodeList

class HTMLOptionElement(HTMLElement):
    """ # GIgnoredStmt
    LegacyFactoryFunction=Option(optional DOMString text = "", optional DOMString value, optional boolean defaultSelected = False, optional boolean selected = False)
    """
    disabled: bool
    form: HTMLFormElement | None
    label: str
    defaultSelected: bool
    selected: bool
    value: str
    text: str
    index: int

class HTMLOptGroupElement(HTMLElement):
    disabled: bool
    label: str

class HTMLButtonElement(HTMLElement):
    disabled: bool
    form: HTMLFormElement | None
    formAction: USVString
    formEnctype: str
    formMethod: str
    formNoValidate: bool
    formTarget: str
    name: str
    type: str
    value: str
    willValidate: bool
    validity: ValidityState
    validationMessage: str
    def checkValidity(self) -> bool: ...
    def reportValidity(self) -> bool: ...
    def setCustomValidity(self, error: str) -> None: ...
    labels: NodeList

class HTMLAnchorElement(HTMLElement, HTMLAttributionSrcElementUtils, HTMLHyperlinkElementUtils):
    target: str
    download: str
    ping: USVString
    rel: str
    relList: DOMTokenList
    hreflang: str
    type: str
    text: str
    referrerPolicy: str
    coords: str
    charset: str
    name: str
    rev: str
    shape: str
    attributionSourceId: int

class HTMLImageElement(HTMLElement, HTMLAttributionSrcElementUtils):
    x: int
    y: int
    """ # GIgnoredStmt
    LegacyFactoryFunction=Image(optional unsigned long width, optional unsigned long height)
    """
    alt: str
    src: USVString
    srcset: USVString
    sizes: str
    crossOrigin: str | None
    useMap: str
    isMap: bool
    width: int
    height: int
    naturalWidth: int
    naturalHeight: int
    complete: bool
    currentSrc: USVString
    referrerPolicy: str
    decoding: str
    loading: str
    def decode(self) -> None: ...
    name: str
    lowsrc: USVString
    align: str
    hspace: int
    vspace: int
    longDesc: USVString
    border: str
    fetchPriority: str

class HTMLCanvasElement(HTMLElement):
    width: int
    height: int
    def getContext(self, contextId: str, options: Any | None = None) -> RenderingContext | None: ...
    def toDataURL(self, type: str | None = "image/png", quality: Any | None = None) -> USVString: ...
    def toBlob(self, callback: BlobCallback, type: str | None = "image/png", quality: Any | None = None) -> None: ...
    def transferControlToOffscreen(self) -> OffscreenCanvas: ...
    def captureStream(self, frameRequestRate: float | None = None) -> MediaStream: ...

class HTMLVideoElement(HTMLMediaElement):
    width: int
    height: int
    videoWidth: int
    videoHeight: int
    poster: USVString
    playsInline: bool
    def getVideoPlaybackQuality(self) -> VideoPlaybackQuality: ...
    def requestPictureInPicture(self) -> PictureInPictureWindow: ...
    onenterpictureinpicture: EventHandler
    onleavepictureinpicture: EventHandler
    disablePictureInPicture: bool
    def requestVideoFrameCallback(self, callback: VideoFrameRequestCallback) -> int: ...
    def cancelVideoFrameCallback(self, handle: int) -> None: ...

class HTMLAudioElement(HTMLMediaElement):
    """ # GIgnoredStmt
    LegacyFactoryFunction=Audio(optional DOMString src)
    """

class HTMLSourceElement(HTMLElement):
    src: USVString
    type: str
    srcset: USVString
    sizes: str
    media: str
    width: int
    height: int

class HTMLMediaElement(HTMLElement):
    sinkId: str
    def setSinkId(self, sinkId: str) -> None: ...
    mediaKeys: MediaKeys | None
    onencrypted: EventHandler
    onwaitingforkey: EventHandler
    def setMediaKeys(self, mediaKeys: MediaKeys | None) -> None: ...
    error: MediaError | None
    src: USVString
    srcObject: MediaProvider | None
    currentSrc: USVString
    crossOrigin: str | None
    NETWORK_EMPTY = 0
    NETWORK_IDLE = 1
    NETWORK_LOADING = 2
    NETWORK_NO_SOURCE = 3
    networkState: int
    preload: str
    buffered: TimeRanges
    def load(self) -> None: ...
    def canPlayType(self, type: str) -> CanPlayTypeResult: ...
    HAVE_NOTHING = 0
    HAVE_METADATA = 1
    HAVE_CURRENT_DATA = 2
    HAVE_FUTURE_DATA = 3
    HAVE_ENOUGH_DATA = 4
    readyState: int
    seeking: bool
    currentTime: float
    def fastSeek(self, time: float) -> None: ...
    duration: float
    def getStartDate(self) -> object: ...
    paused: bool
    defaultPlaybackRate: float
    playbackRate: float
    preservesPitch: bool
    played: TimeRanges
    seekable: TimeRanges
    ended: bool
    autoplay: bool
    loop: bool
    def play(self) -> None: ...
    def pause(self) -> None: ...
    controls: bool
    volume: float
    muted: bool
    defaultMuted: bool
    audioTracks: AudioTrackList
    videoTracks: VideoTrackList
    textTracks: TextTrackList
    def addTextTrack(self, kind: TextTrackKind, label: str | None = "", language: str | None = "") -> TextTrack: ...
    def captureStream(self) -> MediaStream: ...
    remote: RemotePlayback
    disableRemotePlayback: bool

class HTMLIFrameElement(HTMLElement):
    csp: str
    src: USVString
    srcdoc: str
    name: str
    sandbox: DOMTokenList
    allow: str
    allowFullscreen: bool
    width: str
    height: str
    referrerPolicy: str
    loading: str
    contentDocument: Document | None
    contentWindow: WindowProxy | None
    def getSVGDocument(self) -> Document | None: ...
    align: str
    scrolling: str
    frameBorder: str
    longDesc: USVString
    marginHeight: str
    marginWidth: str
    permissionsPolicy: PermissionsPolicy
    fetchPriority: str

class HTMLScriptElement(HTMLElement, HTMLAttributionSrcElementUtils):
    src: USVString
    type: str
    noModule: bool
    async_: bool
    defer: bool
    crossOrigin: str | None
    text: str
    integrity: str
    referrerPolicy: str
    blocking: DOMTokenList
    charset: str
    event: str
    htmlFor: str
    fetchPriority: str

class HTMLStyleElement(HTMLElement, LinkStyle):
    disabled: bool
    media: str
    blocking: DOMTokenList
    type: str

class HTMLLinkElement(HTMLElement, LinkStyle):
    href: USVString
    crossOrigin: str | None
    rel: str
    relList: DOMTokenList
    media: str
    integrity: str
    hreflang: str
    type: str
    sizes: DOMTokenList
    imageSrcset: USVString
    imageSizes: str
    referrerPolicy: str
    blocking: DOMTokenList
    disabled: bool
    charset: str
    rev: str
    target: str
    fetchPriority: str

class HTMLMetaElement(HTMLElement):
    name: str
    httpEquiv: str
    content: str
    media: str
    scheme: str

class HTMLTemplateElement(HTMLElement):
    content: DocumentFragment

class HTMLDialogElement(HTMLElement):
    open: bool
    returnValue: str
    def show(self) -> None: ...
    def showModal(self) -> None: ...
    def close(self, returnValue: str | None = None) -> None: ...

class Window(EventTarget, GlobalEventHandlers, WindowEventHandlers, WindowOrWorkerGlobalScope, AnimationFrameProvider, WindowSessionStorage, WindowLocalStorage):
    orientation: short
    onorientationchange: EventHandler
    cookieStore: CookieStore
    def navigate(self, dir: SpatialNavigationDirection) -> None: ...
    def matchMedia(self, query: CSSOMString) -> MediaQueryList: ...
    screen: Screen
    visualViewport: VisualViewport | None
    def moveTo(self, x: int, y: int) -> None: ...
    def moveBy(self, x: int, y: int) -> None: ...
    def resizeTo(self, width: int, height: int) -> None: ...
    def resizeBy(self, x: int, y: int) -> None: ...
    innerWidth: int
    innerHeight: int
    scrollX: float
    pageXOffset: float
    scrollY: float
    pageYOffset: float
    @overload
    def scroll(self, options: ScrollToOptions | None = {}) -> None: ...
    @overload
    def scroll(self, x: float, y: float) -> None: ...
    @overload
    def scrollTo(self, options: ScrollToOptions | None = {}) -> None: ...
    @overload
    def scrollTo(self, x: float, y: float) -> None: ...
    @overload
    def scrollBy(self, options: ScrollToOptions | None = {}) -> None: ...
    @overload
    def scrollBy(self, x: float, y: float) -> None: ...
    screenX: int
    screenLeft: int
    screenY: int
    screenTop: int
    outerWidth: int
    outerHeight: int
    devicePixelRatio: float
    def getComputedStyle(self, elt: Element, pseudoElt: CSSOMString | None = None) -> CSSStyleDeclaration: ...
    def getDigitalGoodsService(self, serviceProvider: str) -> DigitalGoodsService: ...
    event: Event | None
    def showOpenFilePicker(self, options: OpenFilePickerOptions | None = {}) -> Sequence[FileSystemFileHandle]: ...
    def showSaveFilePicker(self, options: SaveFilePickerOptions | None = {}) -> FileSystemFileHandle: ...
    def showDirectoryPicker(self, options: DirectoryPickerOptions | None = {}) -> FileSystemDirectoryHandle: ...
    window: WindowProxy
    self: WindowProxy
    document: Document
    name: str
    location: Location
    history: History
    customElements: CustomElementRegistry
    locationbar: BarProp
    menubar: BarProp
    personalbar: BarProp
    scrollbars: BarProp
    statusbar: BarProp
    toolbar: BarProp
    status: str
    def close(self) -> None: ...
    closed: bool
    def stop(self) -> None: ...
    def focus(self) -> None: ...
    def blur(self) -> None: ...
    frames: WindowProxy
    length: int
    top: WindowProxy | None
    opener: Any
    parent: WindowProxy | None
    frameElement: Element | None
    def open(self, url: USVString | None = "", target: str | None = "_blank", features: str | None = "") -> WindowProxy | None: ...
    navigator: Navigator
    clientInformation: Navigator
    originAgentCluster: bool
    @overload
    def alert(self) -> None: ...
    @overload
    def alert(self, message: str) -> None: ...
    def confirm(self, message: str | None = "") -> bool: ...
    def prompt(self, message: str | None = "", default: str | None = "") -> str | None: ...
    def print(self) -> None: ...
    @overload
    def postMessage(self, message: Any, targetOrigin: USVString, transfer: Sequence[object] | None = []) -> None: ...
    @overload
    def postMessage(self, message: Any, options: WindowPostMessageOptions | None = {}) -> None: ...
    def captureEvents(self) -> None: ...
    def releaseEvents(self) -> None: ...
    external: External
    def queryLocalFonts(self, options: QueryOptions | None = {}) -> Sequence[FontData]: ...
    onappinstalled: EventHandler
    onbeforeinstallprompt: EventHandler
    navigation: Navigation
    ondeviceorientation: EventHandler
    ondeviceorientationabsolute: EventHandler
    oncompassneedscalibration: EventHandler
    ondevicemotion: EventHandler
    portalHost: PortalHost | None
    def requestIdleCallback(self, callback: IdleRequestCallback, options: IdleRequestOptions | None = {}) -> int: ...
    def cancelIdleCallback(self, handle: int) -> None: ...
    def getSelection(self) -> Selection | None: ...
    speechSynthesis: SpeechSynthesis
    launchQueue: LaunchQueue
    def getScreenDetails(self) -> ScreenDetails: ...

class Location:
    href: USVString
    origin: USVString
    protocol: USVString
    host: USVString
    hostname: USVString
    port: USVString
    pathname: USVString
    search: USVString
    hash: USVString
    def assign(self, url: USVString) -> None: ...
    def replace(self, url: USVString) -> None: ...
    def reload(self) -> None: ...
    ancestorOrigins: DOMStringList

class History:
    length: int
    scrollRestoration: ScrollRestoration
    state: Any
    def go(self, delta: int | None = 0) -> None: ...
    def back(self) -> None: ...
    def forward(self) -> None: ...
    def pushState(self, data: Any, unused: str, url: USVString | None = None) -> None: ...
    def replaceState(self, data: Any, unused: str, url: USVString | None = None) -> None: ...

class Navigator(NavigatorBadge, NavigatorDeviceMemory, NavigatorID, NavigatorLanguage, NavigatorOnLine, NavigatorContentUtils, NavigatorCookies, NavigatorPlugins, NavigatorConcurrentHardware, NavigatorNetworkInformation, NavigatorStorage, NavigatorUA, NavigatorLocks, NavigatorAutomationInformation, NavigatorGPU, NavigatorML):
    @overload
    def getAutoplayPolicy(self, type: AutoplayPolicyMediaType) -> AutoplayPolicy: ...
    @overload
    def getAutoplayPolicy(self, element: HTMLMediaElement) -> AutoplayPolicy: ...
    @overload
    def getAutoplayPolicy(self, context: AudioContext) -> AutoplayPolicy: ...
    def setClientBadge(self, contents: int | None = None) -> None: ...
    def clearClientBadge(self) -> None: ...
    def getBattery(self) -> BatteryManager: ...
    def sendBeacon(self, url: USVString, data: BodyInit | None = None) -> bool: ...
    clipboard: Clipboard
    contacts: ContactsManager
    credentials: CredentialsContainer
    devicePosture: DevicePosture
    def requestMediaKeySystemAccess(self, keySystem: str, supportedConfigurations: Sequence[MediaKeySystemConfiguration]) -> MediaKeySystemAccess: ...
    epubReadingSystem: EpubReadingSystem
    def getGamepads(self) -> Sequence[Gamepad | None]: ...
    geolocation: Geolocation
    def getInstalledRelatedApps(self) -> Sequence[RelatedApplication]: ...
    userActivation: UserActivation
    ink: Ink
    scheduling: Scheduling
    keyboard: Keyboard
    mediaCapabilities: MediaCapabilities
    mediaDevices: MediaDevices
    def getUserMedia(self, constraints: MediaStreamConstraints, successCallback: NavigatorUserMediaSuccessCallback, errorCallback: NavigatorUserMediaErrorCallback) -> None: ...
    mediaSession: MediaSession
    permissions: Permissions
    maxTouchPoints: int
    presentation: Presentation
    wakeLock: WakeLock
    serial: Serial
    serviceWorker: ServiceWorkerContainer
    def vibrate(self, pattern: VibratePattern) -> bool: ...
    virtualKeyboard: VirtualKeyboard
    bluetooth: Bluetooth
    def share(self, data: ShareData | None = {}) -> None: ...
    def canShare(self, data: ShareData | None = {}) -> bool: ...
    hid: HID
    def requestMIDIAccess(self, options: MIDIOptions | None = {}) -> MIDIAccess: ...
    usb: USB
    xr: XRSystem
    windowControlsOverlay: WindowControlsOverlay

class Storage:
    """Web Storage API interface for localStorage and sessionStorage."""
    length: int
    def key(self, index: int) -> str | None: ...
    def getItem(self, key: str) -> str | None: ...
    def setItem(self, key: str, value: str) -> None: ...
    def removeItem(self, key: str) -> None: ...
    def clear(self) -> None: ...

class ConsoleNamespace:
    def assert_(self, condition: bool | None = False, *data: Any) -> None: ...
    def clear(self) -> None: ...
    def debug(self, *data: Any) -> None: ...
    def error(self, *data: Any) -> None: ...
    def info(self, *data: Any) -> None: ...
    def log(self, *data: Any) -> None: ...
    def table(self, tabularData: Any | None = None, properties: Sequence[str] | None = None) -> None: ...
    def trace(self, *data: Any) -> None: ...
    def warn(self, *data: Any) -> None: ...
    def dir(self, item: Any | None = None, options: object | None = None) -> None: ...
    def dirxml(self, *data: Any) -> None: ...
    def count(self, label: str | None = "default") -> None: ...
    def countReset(self, label: str | None = "default") -> None: ...
    def group(self, *data: Any) -> None: ...
    def groupCollapsed(self, *data: Any) -> None: ...
    def groupEnd(self) -> None: ...
    def time(self, label: str | None = "default") -> None: ...
    def timeLog(self, label: str | None = "default", *data: Any) -> None: ...
    def timeEnd(self, label: str | None = "default") -> None: ...

class Clipboard(EventTarget):
    def read(self) -> ClipboardItems: ...
    def readText(self) -> str: ...
    def write(self, data: ClipboardItems) -> None: ...
    def writeText(self, data: str) -> None: ...

class Geolocation:
    def getCurrentPosition(self, successCallback: PositionCallback, errorCallback: PositionErrorCallback | None = None, options: PositionOptions | None = {}) -> None: ...
    def watchPosition(self, successCallback: PositionCallback, errorCallback: PositionErrorCallback | None = None, options: PositionOptions | None = {}) -> int: ...
    def clearWatch(self, watchId: int) -> None: ...

class Screen:
    availWidth: int
    availHeight: int
    width: int
    height: int
    colorDepth: int
    pixelDepth: int
    orientation: ScreenOrientation
    isExtended: bool
    onchange: EventHandler

class CSSStyleDeclaration:
    cssText: CSSOMString
    length: int
    def getPropertyValue(self, property: CSSOMString) -> CSSOMString: ...
    def getPropertyPriority(self, property: CSSOMString) -> CSSOMString: ...
    def setProperty(self, property: CSSOMString, value: CSSOMString, priority: CSSOMString | None = "") -> None: ...
    def removeProperty(self, property: CSSOMString) -> CSSOMString: ...
    parentRule: CSSRule | None
    cssFloat: CSSOMString
    accentColor: str
    additiveSymbols: str
    alignContent: str
    alignItems: str
    alignSelf: str
    alignmentBaseline: str
    all: str
    animation: str
    animationComposition: str
    animationDelay: str
    animationDirection: str
    animationDuration: str
    animationFillMode: str
    animationIterationCount: str
    animationName: str
    animationPlayState: str
    animationTimingFunction: str
    appRegion: str
    appearance: str
    ascentOverride: str
    aspectRatio: str
    backdropFilter: str
    backfaceVisibility: str
    background: str
    backgroundAttachment: str
    backgroundBlendMode: str
    backgroundClip: str
    backgroundColor: str
    backgroundImage: str
    backgroundOrigin: str
    backgroundPosition: str
    backgroundPositionX: str
    backgroundPositionY: str
    backgroundRepeat: str
    backgroundRepeatX: str
    backgroundRepeatY: str
    backgroundSize: str
    basePalette: str
    baselineShift: str
    baselineSource: str
    blockSize: str
    border: str
    borderBlock: str
    borderBlockColor: str
    borderBlockEnd: str
    borderBlockEndColor: str
    borderBlockEndStyle: str
    borderBlockEndWidth: str
    borderBlockStart: str
    borderBlockStartColor: str
    borderBlockStartStyle: str
    borderBlockStartWidth: str
    borderBlockStyle: str
    borderBlockWidth: str
    borderBottom: str
    borderBottomColor: str
    borderBottomLeftRadius: str
    borderBottomRightRadius: str
    borderBottomStyle: str
    borderBottomWidth: str
    borderCollapse: str
    borderColor: str
    borderEndEndRadius: str
    borderEndStartRadius: str
    borderImage: str
    borderImageOutset: str
    borderImageRepeat: str
    borderImageSlice: str
    borderImageSource: str
    borderImageWidth: str
    borderInline: str
    borderInlineColor: str
    borderInlineEnd: str
    borderInlineEndColor: str
    borderInlineEndStyle: str
    borderInlineEndWidth: str
    borderInlineStart: str
    borderInlineStartColor: str
    borderInlineStartStyle: str
    borderInlineStartWidth: str
    borderInlineStyle: str
    borderInlineWidth: str
    borderLeft: str
    borderLeftColor: str
    borderLeftStyle: str
    borderLeftWidth: str
    borderRadius: str
    borderRight: str
    borderRightColor: str
    borderRightStyle: str
    borderRightWidth: str
    borderSpacing: str
    borderStartEndRadius: str
    borderStartStartRadius: str
    borderStyle: str
    borderTop: str
    borderTopColor: str
    borderTopLeftRadius: str
    borderTopRightRadius: str
    borderTopStyle: str
    borderTopWidth: str
    borderWidth: str
    bottom: str
    boxShadow: str
    boxSizing: str
    breakAfter: str
    breakBefore: str
    breakInside: str
    bufferedRendering: str
    captionSide: str
    caretColor: str
    clear: str
    clip: str
    clipPath: str
    clipRule: str
    color: str
    colorInterpolation: str
    colorInterpolationFilters: str
    colorRendering: str
    colorScheme: str
    columnCount: str
    columnFill: str
    columnGap: str
    columnRule: str
    columnRuleColor: str
    columnRuleStyle: str
    columnRuleWidth: str
    columnSpan: str
    columnWidth: str
    columns: str
    contain: str
    containIntrinsicBlockSize: str
    containIntrinsicHeight: str
    containIntrinsicInlineSize: str
    containIntrinsicSize: str
    containIntrinsicWidth: str
    container: str
    containerName: str
    containerType: str
    content: str
    contentVisibility: str
    counterIncrement: str
    counterReset: str
    counterSet: str
    cursor: str
    cx: str
    cy: str
    descentOverride: str
    direction: str
    display: str
    dominantBaseline: str
    emptyCells: str
    fallback: str
    fill: str
    fillOpacity: str
    fillRule: str
    filter: str
    flex: str
    flexBasis: str
    flexDirection: str
    flexFlow: str
    flexGrow: str
    flexShrink: str
    flexWrap: str
    floodColor: str
    floodOpacity: str
    font: str
    fontDisplay: str
    fontFamily: str
    fontFeatureSettings: str
    fontKerning: str
    fontOpticalSizing: str
    fontPalette: str
    fontSize: str
    fontStretch: str
    fontStyle: str
    fontSynthesis: str
    fontSynthesisSmallCaps: str
    fontSynthesisStyle: str
    fontSynthesisWeight: str
    fontVariant: str
    fontVariantAlternates: str
    fontVariantCaps: str
    fontVariantEastAsian: str
    fontVariantLigatures: str
    fontVariantNumeric: str
    fontVariationSettings: str
    fontWeight: str
    forcedColorAdjust: str
    gap: str
    grid: str
    gridArea: str
    gridAutoColumns: str
    gridAutoFlow: str
    gridAutoRows: str
    gridColumn: str
    gridColumnEnd: str
    gridColumnGap: str
    gridColumnStart: str
    gridGap: str
    gridRow: str
    gridRowEnd: str
    gridRowGap: str
    gridRowStart: str
    gridTemplate: str
    gridTemplateAreas: str
    gridTemplateColumns: str
    gridTemplateRows: str
    height: str
    hyphenateCharacter: str
    hyphenateLimitChars: str
    hyphens: str
    imageOrientation: str
    imageRendering: str
    inherits: str
    initialLetter: str
    initialValue: str
    inlineSize: str
    inset: str
    insetBlock: str
    insetBlockEnd: str
    insetBlockStart: str
    insetInline: str
    insetInlineEnd: str
    insetInlineStart: str
    isolation: str
    justifyContent: str
    justifyItems: str
    justifySelf: str
    left: str
    letterSpacing: str
    lightingColor: str
    lineBreak: str
    lineGapOverride: str
    lineHeight: str
    listStyle: str
    listStyleImage: str
    listStylePosition: str
    listStyleType: str
    margin: str
    marginBlock: str
    marginBlockEnd: str
    marginBlockStart: str
    marginBottom: str
    marginInline: str
    marginInlineEnd: str
    marginInlineStart: str
    marginLeft: str
    marginRight: str
    marginTop: str
    marker: str
    markerEnd: str
    markerMid: str
    markerStart: str
    mask: str
    maskType: str
    mathDepth: str
    mathShift: str
    mathStyle: str
    maxBlockSize: str
    maxHeight: str
    maxInlineSize: str
    maxWidth: str
    minBlockSize: str
    minHeight: str
    minInlineSize: str
    minWidth: str
    mixBlendMode: str
    negative: str
    objectFit: str
    objectPosition: str
    objectViewBox: str
    offset: str
    offsetDistance: str
    offsetPath: str
    offsetRotate: str
    opacity: str
    order: str
    orphans: str
    outline: str
    outlineColor: str
    outlineOffset: str
    outlineStyle: str
    outlineWidth: str
    overflow: str
    overflowAnchor: str
    overflowClipMargin: str
    overflowWrap: str
    overflowX: str
    overflowY: str
    overrideColors: str
    overscrollBehavior: str
    overscrollBehaviorBlock: str
    overscrollBehaviorInline: str
    overscrollBehaviorX: str
    overscrollBehaviorY: str
    pad: str
    padding: str
    paddingBlock: str
    paddingBlockEnd: str
    paddingBlockStart: str
    paddingBottom: str
    paddingInline: str
    paddingInlineEnd: str
    paddingInlineStart: str
    paddingLeft: str
    paddingRight: str
    paddingTop: str
    page: str
    pageBreakAfter: str
    pageBreakBefore: str
    pageBreakInside: str
    pageOrientation: str
    paintOrder: str
    perspective: str
    perspectiveOrigin: str
    placeContent: str
    placeItems: str
    placeSelf: str
    pointerEvents: str
    position: str
    prefix: str
    quotes: str
    range: str
    resize: str
    right: str
    rotate: str
    rowGap: str
    rubyPosition: str
    rx: str
    ry: str
    scale: str
    scrollBehavior: str
    scrollMargin: str
    scrollMarginBlock: str
    scrollMarginBlockEnd: str
    scrollMarginBlockStart: str
    scrollMarginBottom: str
    scrollMarginInline: str
    scrollMarginInlineEnd: str
    scrollMarginInlineStart: str
    scrollMarginLeft: str
    scrollMarginRight: str
    scrollMarginTop: str
    scrollPadding: str
    scrollPaddingBlock: str
    scrollPaddingBlockEnd: str
    scrollPaddingBlockStart: str
    scrollPaddingBottom: str
    scrollPaddingInline: str
    scrollPaddingInlineEnd: str
    scrollPaddingInlineStart: str
    scrollPaddingLeft: str
    scrollPaddingRight: str
    scrollPaddingTop: str
    scrollSnapAlign: str
    scrollSnapStop: str
    scrollSnapType: str
    scrollbarGutter: str
    shapeImageThreshold: str
    shapeMargin: str
    shapeOutside: str
    shapeRendering: str
    size: str
    sizeAdjust: str
    speak: str
    speakAs: str
    src: str
    stopColor: str
    stopOpacity: str
    stroke: str
    strokeDasharray: str
    strokeDashoffset: str
    strokeLinecap: str
    strokeLinejoin: str
    strokeMiterlimit: str
    strokeOpacity: str
    strokeWidth: str
    suffix: str
    symbols: str
    syntax: str
    system: str
    tabSize: str
    tableLayout: str
    textAlign: str
    textAlignLast: str
    textAnchor: str
    textCombineUpright: str
    textDecoration: str
    textDecorationColor: str
    textDecorationLine: str
    textDecorationSkipInk: str
    textDecorationStyle: str
    textDecorationThickness: str
    textEmphasis: str
    textEmphasisColor: str
    textEmphasisPosition: str
    textEmphasisStyle: str
    textIndent: str
    textOrientation: str
    textOverflow: str
    textRendering: str
    textShadow: str
    textSizeAdjust: str
    textTransform: str
    textUnderlineOffset: str
    textUnderlinePosition: str
    top: str
    touchAction: str
    transform: str
    transformBox: str
    transformOrigin: str
    transformStyle: str
    transition: str
    transitionDelay: str
    transitionDuration: str
    transitionProperty: str
    transitionTimingFunction: str
    translate: str
    unicodeBidi: str
    unicodeRange: str
    userSelect: str
    vectorEffect: str
    verticalAlign: str
    viewTransitionName: str
    visibility: str
    whiteSpace: str
    widows: str
    width: str
    willChange: str
    wordBreak: str
    wordSpacing: str
    wordWrap: str
    writingMode: str
    zIndex: str
    zoom: str

class CSSStyleSheet(StyleSheet):
    ownerRule: CSSRule | None
    cssRules: CSSRuleList
    def insertRule(self, rule: CSSOMString, index: int | None = 0) -> int: ...
    def deleteRule(self, index: int) -> None: ...
    def replace(self, text: USVString) -> CSSStyleSheet: ...
    def replaceSync(self, text: USVString) -> None: ...
    rules: CSSRuleList
    def addRule(self, selector: str | None = "undefined", style: str | None = "undefined", index: int | None = None) -> int: ...
    def removeRule(self, index: int | None = 0) -> None: ...

class StyleSheet:
    type: CSSOMString
    href: USVString | None
    ownerNode: Element | ProcessingInstruction | None
    parentStyleSheet: CSSStyleSheet | None
    title: str | None
    media: MediaList
    disabled: bool

class MediaQueryList(EventTarget):
    media: CSSOMString
    matches: bool
    def addListener(self, callback: EventListener | None) -> None: ...
    def removeListener(self, callback: EventListener | None) -> None: ...
    onchange: EventHandler

class File(Blob):
    name: str
    lastModified: int
    webkitRelativePath: USVString

class FileList:
    length: int

class Blob:
    size: int
    type: str
    def slice(self, start: int | None = None, end: int | None = None, contentType: str | None = None) -> Blob: ...
    def stream(self) -> ReadableStream: ...
    def text(self) -> USVString: ...
    def arrayBuffer(self) -> ArrayBuffer: ...

class FileReader(EventTarget):
    def readAsArrayBuffer(self, blob: Blob) -> None: ...
    def readAsBinaryString(self, blob: Blob) -> None: ...
    def readAsText(self, blob: Blob, encoding: str | None = None) -> None: ...
    def readAsDataURL(self, blob: Blob) -> None: ...
    def abort(self) -> None: ...
    EMPTY = 0
    LOADING = 1
    DONE = 2
    readyState: int
    result: str | ArrayBuffer | None
    error: DOMException | None
    onloadstart: EventHandler
    onprogress: EventHandler
    onload: EventHandler
    onabort: EventHandler
    onerror: EventHandler
    onloadend: EventHandler

class DataTransfer:
    dropEffect: str
    effectAllowed: str
    items: DataTransferItemList
    def setDragImage(self, image: Element, x: int, y: int) -> None: ...
    types: Sequence[str]
    def getData(self, format: str) -> str: ...
    def setData(self, format: str, data: str) -> None: ...
    def clearData(self, format: str | None = None) -> None: ...
    files: FileList

class DataTransferItem:
    def webkitGetAsEntry(self) -> FileSystemEntry | None: ...
    def getAsFileSystemHandle(self) -> FileSystemHandle | None: ...
    kind: str
    type: str
    def getAsString(self, callback: FunctionStringCallback | None) -> None: ...
    def getAsFile(self) -> File | None: ...

class DataTransferItemList:
    length: int
    @overload
    def add(self, data: str, type: str) -> DataTransferItem | None: ...
    @overload
    def add(self, data: File) -> DataTransferItem | None: ...
    def remove(self, index: int) -> None: ...
    def clear(self) -> None: ...

class Range(AbstractRange):
    def createContextualFragment(self, fragment: str) -> DocumentFragment: ...
    def getClientRects(self) -> DOMRectList: ...
    def getBoundingClientRect(self) -> DOMRect: ...
    commonAncestorContainer: Node
    def setStart(self, node: Node, offset: int) -> None: ...
    def setEnd(self, node: Node, offset: int) -> None: ...
    def setStartBefore(self, node: Node) -> None: ...
    def setStartAfter(self, node: Node) -> None: ...
    def setEndBefore(self, node: Node) -> None: ...
    def setEndAfter(self, node: Node) -> None: ...
    def collapse(self, toStart: bool | None = False) -> None: ...
    def selectNode(self, node: Node) -> None: ...
    def selectNodeContents(self, node: Node) -> None: ...
    START_TO_START = 0
    START_TO_END = 1
    END_TO_END = 2
    END_TO_START = 3
    def compareBoundaryPoints(self, how: int, sourceRange: Range) -> short: ...
    def deleteContents(self) -> None: ...
    def extractContents(self) -> DocumentFragment: ...
    def cloneContents(self) -> DocumentFragment: ...
    def insertNode(self, node: Node) -> None: ...
    def surroundContents(self, newParent: Node) -> None: ...
    def cloneRange(self) -> Range: ...
    def detach(self) -> None: ...
    def isPointInRange(self, node: Node, offset: int) -> bool: ...
    def comparePoint(self, node: Node, offset: int) -> short: ...
    def intersectsNode(self, node: Node) -> bool: ...

class Selection:
    anchorNode: Node | None
    anchorOffset: int
    focusNode: Node | None
    focusOffset: int
    isCollapsed: bool
    rangeCount: int
    type: str
    def getRangeAt(self, index: int) -> Range: ...
    def addRange(self, range: Range) -> None: ...
    def removeRange(self, range: Range) -> None: ...
    def removeAllRanges(self) -> None: ...
    def empty(self) -> None: ...
    def getComposedRange(self, *shadowRoots: ShadowRoot) -> StaticRange: ...
    def collapse(self, node: Node | None, offset: int | None = 0) -> None: ...
    def setPosition(self, node: Node | None, offset: int | None = 0) -> None: ...
    def collapseToStart(self) -> None: ...
    def collapseToEnd(self) -> None: ...
    def extend(self, node: Node, offset: int | None = 0) -> None: ...
    def setBaseAndExtent(self, anchorNode: Node, anchorOffset: int, focusNode: Node, focusOffset: int) -> None: ...
    def selectAllChildren(self, node: Node) -> None: ...
    def modify(self, alter: str | None = None, direction: str | None = None, granularity: str | None = None) -> None: ...
    def deleteFromDocument(self) -> None: ...
    def containsNode(self, node: Node, allowPartialContainment: bool | None = False) -> bool: ...

class MutationObserver:
    def observe(self, target: Node, options: MutationObserverInit | None = {}) -> None: ...
    def disconnect(self) -> None: ...
    def takeRecords(self) -> Sequence[MutationRecord]: ...

class MutationRecord:
    type: str
    target: Node
    addedNodes: NodeList
    removedNodes: NodeList
    previousSibling: Node | None
    nextSibling: Node | None
    attributeName: str | None
    attributeNamespace: str | None
    oldValue: str | None

class IntersectionObserver:
    root: Element | Document | None
    rootMargin: str
    thresholds: Sequence[float]
    def observe(self, target: Element) -> None: ...
    def unobserve(self, target: Element) -> None: ...
    def disconnect(self) -> None: ...
    def takeRecords(self) -> Sequence[IntersectionObserverEntry]: ...

class IntersectionObserverEntry:
    time: DOMHighResTimeStamp
    rootBounds: DOMRectReadOnly | None
    boundingClientRect: DOMRectReadOnly
    intersectionRect: DOMRectReadOnly
    isIntersecting: bool
    intersectionRatio: float
    target: Element

class ResizeObserver:
    def observe(self, target: Element, options: ResizeObserverOptions | None = {}) -> None: ...
    def unobserve(self, target: Element) -> None: ...
    def disconnect(self) -> None: ...

class ResizeObserverEntry:
    target: Element
    contentRect: DOMRectReadOnly
    borderBoxSize: Sequence[ResizeObserverSize]
    contentBoxSize: Sequence[ResizeObserverSize]
    devicePixelContentBoxSize: Sequence[ResizeObserverSize]

class CanvasRenderingContext2D(CanvasState, CanvasTransform, CanvasCompositing, CanvasImageSmoothing, CanvasFillStrokeStyles, CanvasShadowStyles, CanvasFilters, CanvasRect, CanvasDrawPath, CanvasUserInterface, CanvasText, CanvasDrawImage, CanvasImageData, CanvasPathDrawingStyles, CanvasTextDrawingStyles, CanvasPath):
    canvas: HTMLCanvasElement
    def getContextAttributes(self) -> CanvasRenderingContext2DSettings: ...

class ImageData:
    width: int
    height: int
    data: Uint8ClampedArray
    colorSpace: PredefinedColorSpace

class Path2D(CanvasPath):
    def addPath(self, path: Path2D, transform: DOMMatrix2DInit | None = {}) -> None: ...

class URL:
    href: USVString
    origin: USVString
    protocol: USVString
    username: USVString
    password: USVString
    host: USVString
    hostname: USVString
    port: USVString
    pathname: USVString
    search: USVString
    searchParams: URLSearchParams
    hash: USVString
    def toJSON(self) -> USVString: ...

class URLSearchParams:
    def append(self, name: USVString, value: USVString) -> None: ...
    def delete(self, name: USVString) -> None: ...
    def get(self, name: USVString) -> USVString | None: ...
    def getAll(self, name: USVString) -> Sequence[USVString]: ...
    def has(self, name: USVString) -> bool: ...
    def set(self, name: USVString, value: USVString) -> None: ...
    def sort(self) -> None: ...

class Headers:
    def append(self, name: ByteString, value: ByteString) -> None: ...
    def delete(self, name: ByteString) -> None: ...
    def get(self, name: ByteString) -> ByteString | None: ...
    def has(self, name: ByteString) -> bool: ...
    def set(self, name: ByteString, value: ByteString) -> None: ...

class Request(Body):
    method: ByteString
    url: USVString
    headers: Headers
    destination: RequestDestination
    referrer: USVString
    referrerPolicy: ReferrerPolicy
    mode: RequestMode
    credentials: RequestCredentials
    cache: RequestCache
    redirect: RequestRedirect
    integrity: str
    keepalive: bool
    isReloadNavigation: bool
    isHistoryNavigation: bool
    signal: AbortSignal
    duplex: RequestDuplex
    def clone(self) -> Request: ...

class Response(Body):
    type: ResponseType
    url: USVString
    redirected: bool
    status: int
    ok: bool
    statusText: ByteString
    headers: Headers
    def clone(self) -> Response: ...

class DOMStringMap: ...

class DOMParser:
    def parseFromString(self, string: str, type: DOMParserSupportedType) -> Document: ...

class XMLSerializer:
    def serializeToString(self, root: Node) -> str: ...

class FormData:
    @overload
    def append(self, name: USVString, value: USVString) -> None: ...
    @overload
    def append(self, name: USVString, blobValue: Blob, filename: USVString | None = None) -> None: ...
    def delete(self, name: USVString) -> None: ...
    def get(self, name: USVString) -> FormDataEntryValue | None: ...
    def getAll(self, name: USVString) -> Sequence[FormDataEntryValue]: ...
    def has(self, name: USVString) -> bool: ...
    @overload
    def set(self, name: USVString, value: USVString) -> None: ...
    @overload
    def set(self, name: USVString, blobValue: Blob, filename: USVString | None = None) -> None: ...

class AbortController:
    signal: AbortSignal
    def abort(self, reason: Any | None = None) -> None: ...

class AbortSignal(EventTarget):
    aborted: bool
    reason: Any
    def throwIfAborted(self) -> None: ...
    onabort: EventHandler


# Type aliases for compatibility
Console = ConsoleNamespace

# USVString and ByteString are just str in Python
USVString = str
ByteString = str
CSSOMString = str

# WebIDL numeric types
short = int
DOMHighResTimeStamp = float

# Undefined types from webtypy - aliased to Any for compatibility
# These are WebIDL types not fully implemented in webtypy
AbstractRange = Any
AddEventListenerOptions = Any
Animation = Any
AnimationEventInit = Any
AnimationFrameProvider = Any
Anvil = Any
ArrayBuffer = Any
Attr = Any
AudioContext = Any
AudioTrackList = Any
AutoplayPolicy = Any
AutoplayPolicyMediaType = Any
BarProp = Any
BatteryManager = Any
BlobCallback = Any
BlobPart = Any
BlobPropertyBag = Any
Bluetooth = Any
Body = Any
BodyInit = Any
BoxQuadOptions = Any
CDATASection = Any
CSSPseudoElement = Any
CSSRule = Any
CSSRuleList = Any
CSSStyleSheetInit = Any
CanPlayTypeResult = Any
CanvasCompositing = Any
CanvasDrawImage = Any
CanvasDrawPath = Any
CanvasFillStrokeStyles = Any
CanvasFilters = Any
CanvasImageData = Any
CanvasImageSmoothing = Any
CanvasPath = Any
CanvasPathDrawingStyles = Any
CanvasRect = Any
CanvasRenderingContext2DSettings = Any
CanvasShadowStyles = Any
CanvasState = Any
CanvasText = Any
CanvasTextDrawingStyles = Any
CanvasTransform = Any
CanvasUserInterface = Any
CaretPosition = Any
CheckVisibilityOptions = Any
ClipboardEventInit = Any
ClipboardItems = Any
Comment = Any
ContactsManager = Any
ConvertCoordinateOptions = Any
CookieStore = Any
CredentialsContainer = Any
CustomElementRegistry = Any
CustomEventInit = Any
DOMException = Any
DOMImplementation = Any
DOMMatrix2DInit = Any
DOMParserSupportedType = Any
DOMPoint = Any
DOMPointInit = Any
DOMQuad = Any
DOMQuadInit = Any
DOMRectList = Any
DOMStringList = Any
DevicePosture = Any
DigitalGoodsService = Any
DirectoryPickerOptions = Any
DocumentReadyState = Any
DocumentTimeline = Any
DocumentType = Any
DocumentVisibilityState = Any
DragEventInit = Any
ELEMENT_NODE = Any
EditContext = Any
ElementCreationOptions = Any
ElementInternals = Any
EpubReadingSystem = Any
ErrorEventInit = Any
EventHandler = Any
EventInit = Any
EventListener = Any
EventListenerOptions = Any
External = Any
FilePropertyBag = Any
FileSystemDirectoryHandle = Any
FileSystemEntry = Any
FileSystemFileHandle = Any
FileSystemHandle = Any
FocusEventInit = Any
FocusOptions = Any
FocusableAreasOption = Any
FontData = Any
FontFaceSet = Any
FontMetrics = Any
FormDataEntryValue = Any
FormDataEventInit = Any
FragmentDirective = Any
FullscreenOptions = Any
FunctionStringCallback = Any
GENERATED = Any
Gamepad = Any
GeometryNode = Any
GetAnimationsOptions = Any
GetRootNodeOptions = Any
HID = Any
HTMLAllCollection = Any
HTMLAttributionSrcElementUtils = Any
HTMLDataListElement = Any
HTMLFormControlsCollection = Any
HTMLHeadElement = Any
HTMLHyperlinkElementUtils = Any
HTMLOptionsCollection = Any
HTMLOrSVGScriptElement = Any
HTMLSlotElement = Any
HTMLTableCaptionElement = Any
HashChangeEventInit = Any
HeadersInit = Any
IdleRequestCallback = Any
IdleRequestOptions = Any
ImageDataSettings = Any
Ink = Any
InputDeviceCapabilities = Any
InputEventInit = Any
IntersectionObserverCallback = Any
IntersectionObserverEntryInit = Any
IntersectionObserverInit = Any
Keyboard = Any
KeyboardEventInit = Any
KeyframeAnimationOptions = Any
LaunchQueue = Any
LinkStyle = Any
MIDIAccess = Any
MIDIOptions = Any
MediaCapabilities = Any
MediaDevices = Any
MediaError = Any
MediaKeySystemAccess = Any
MediaKeySystemConfiguration = Any
MediaKeys = Any
MediaList = Any
MediaProvider = Any
MediaSession = Any
MediaStream = Any
MediaStreamConstraints = Any
MessageEventInit = Any
MessageEventSource = Any
MessagePort = Any
MouseEventInit = Any
MutationCallback = Any
MutationObserverInit = Any
NamedFlowMap = Any
NamedNodeMap = Any
Navigation = Any
NavigatorAutomationInformation = Any
NavigatorBadge = Any
NavigatorConcurrentHardware = Any
NavigatorContentUtils = Any
NavigatorCookies = Any
NavigatorDeviceMemory = Any
NavigatorGPU = Any
NavigatorID = Any
NavigatorLanguage = Any
NavigatorLocks = Any
NavigatorML = Any
NavigatorNetworkInformation = Any
NavigatorOnLine = Any
NavigatorPlugins = Any
NavigatorStorage = Any
NavigatorUA = Any
NavigatorUserMediaErrorCallback = Any
NavigatorUserMediaSuccessCallback = Any
NodeFilter = Any
NodeIterator = Any
OffscreenCanvas = Any
OnErrorEventHandler = Any
OpenFilePickerOptions = Any
Permissions = Any
PermissionsPolicy = Any
PictureInPictureWindow = Any
PointerEventInit = Any
PopStateEventInit = Any
PortalHost = Any
PositionCallback = Any
PositionErrorCallback = Any
PositionOptions = Any
PredefinedColorSpace = Any
Presentation = Any
ProcessingInstruction = Any
ProgressEventInit = Any
QueryOptions = Any
ReadableStream = Any
ReferrerPolicy = Any
RelatedApplication = Any
RemotePlayback = Any
RenderingContext = Any
RequestCache = Any
RequestCredentials = Any
RequestDestination = Any
RequestDuplex = Any
RequestInfo = Any
RequestInit = Any
RequestMode = Any
RequestRedirect = Any
ResizeObserverCallback = Any
ResizeObserverOptions = Any
ResizeObserverSize = Any
ResponseInit = Any
ResponseType = Any
SVGSVGElement = Any
SaveFilePickerOptions = Any
Scheduling = Any
ScreenDetails = Any
ScreenOrientation = Any
ScrollIntoViewOptions = Any
ScrollRestoration = Any
ScrollToOptions = Any
SelectionMode = Any
Serial = Any
ServiceWorkerContainer = Any
SetHTMLOptions = Any
ShadowRoot = Any
ShadowRootInit = Any
ShareData = Any
SpatialNavigationDirection = Any
SpatialNavigationSearchOptions = Any
SpeechSynthesis = Any
StaticRange = Any
StorageEventInit = Any
StylePropertyMap = Any
StylePropertyMapReadOnly = Any
StyleSheetList = Any
SubmitEventInit = Any
Text = Any
TextTrack = Any
TextTrackKind = Any
TextTrackList = Any
TimeRanges = Any
TouchEventInit = Any
TouchInit = Any
TouchType = Any
TransitionEventInit = Any
TreeWalker = Any
UIEventInit = Any
USB = Any
Uint8ClampedArray = Any
UpdateCallback = Any
UserActivation = Any
ValidityState = Any
VibratePattern = Any
VideoFrameRequestCallback = Any
VideoPlaybackQuality = Any
VideoTrackList = Any
ViewTransition = Any
VirtualKeyboard = Any
VisualViewport = Any
WakeLock = Any
WheelEventInit = Any
WindowControlsOverlay = Any
WindowEventHandlers = Any
WindowLocalStorage = Any
WindowOrWorkerGlobalScope = Any
WindowPostMessageOptions = Any
WindowProxy = Any
WindowSessionStorage = Any
XPathExpression = Any
XPathNSResolver = Any
XPathResult = Any
XRSystem = Any


# =============================================================================
# Window module-level exports
# =============================================================================

# The window object itself
window: Window
"""The global window object. Equivalent to `self` in JavaScript."""

# Window properties exported as module-level attributes
document: Document
"""The document associated with the window."""

location: Location
"""The location (URL) of the window."""

history: History
"""The browser's session history."""

navigator: Navigator
"""Information about the browser/user agent."""

localStorage: Storage
"""Storage that persists across browser sessions."""

sessionStorage: Storage
"""Storage that lasts for the duration of the page session."""

console: Console
"""The browser's debugging console."""

# Window dimensions
innerWidth: int
"""The interior width of the window in pixels."""

innerHeight: int
"""The interior height of the window in pixels."""

outerWidth: int
"""The width of the outside of the browser window."""

outerHeight: int
"""The height of the outside of the browser window."""

# Scroll position
scrollX: float
"""The number of pixels scrolled horizontally."""

scrollY: float
"""The number of pixels scrolled vertically."""

pageXOffset: float
"""Alias for scrollX."""

pageYOffset: float
"""Alias for scrollY."""

# Screen position
screenX: int
"""The horizontal distance from the left screen edge."""

screenY: int
"""The vertical distance from the top screen edge."""

screenLeft: int
"""Alias for screenX."""

screenTop: int
"""Alias for screenY."""

# Device info
devicePixelRatio: float
"""The ratio between physical pixels and CSS pixels."""

# Window state
name: str
"""The name of the window."""

closed: bool
"""Whether the window has been closed."""


# Window methods (commonly used)
def alert(message: str = "") -> None:
    """Display an alert dialog."""
    ...


def confirm(message: str = "") -> bool:
    """Display a confirmation dialog."""
    ...


def prompt(message: str = "", default: str = "") -> str | None:
    """Display a prompt dialog."""
    ...


def open(
    url: str = "",
    target: str = "_blank",
    features: str = "",
) -> object | None:
    """Open a new browser window."""
    ...


def close() -> None:
    """Close the window."""
    ...


def focus() -> None:
    """Focus the window."""
    ...


def blur() -> None:
    """Remove focus from the window."""
    ...


def scroll(x: float | dict[str, object], y: float | None = None) -> None:
    """Scroll to a position in the document."""
    ...


def scrollTo(x: float | dict[str, object], y: float | None = None) -> None:
    """Scroll to a position in the document."""
    ...


def scrollBy(x: float | dict[str, object], y: float | None = None) -> None:
    """Scroll by an amount."""
    ...


def requestAnimationFrame(callback: object) -> int:
    """Request an animation frame callback."""
    ...


def cancelAnimationFrame(handle: int) -> None:
    """Cancel an animation frame callback."""
    ...


def setTimeout(callback: object, delay: int = 0, *args: object) -> int:
    """Set a timer to execute a callback."""
    ...


def clearTimeout(id: int) -> None:
    """Clear a timer."""
    ...


def setInterval(callback: object, delay: int = 0, *args: object) -> int:
    """Set a recurring timer."""
    ...


def clearInterval(id: int) -> None:
    """Clear a recurring timer."""
    ...


def fetch(input: str | object, init: dict[str, object] | None = None) -> object:
    """Fetch a resource from the network."""
    ...


def getComputedStyle(elt: object, pseudoElt: str | None = None) -> object:
    """Get computed styles for an element."""
    ...


def matchMedia(query: str) -> object:
    """Match a media query."""
    ...


def atob(data: str) -> str:
    """Decode a base64-encoded string."""
    ...


def btoa(data: str) -> str:
    """Encode a string to base64."""
    ...


def postMessage(
    message: object, targetOrigin: str, transfer: list[object] | None = None
) -> None:
    """Post a message to another window."""
    ...


def print() -> None:
    """Print the document."""
    ...


def stop() -> None:
    """Stop loading the document."""
    ...


def getSelection() -> object | None:
    """Get the current text selection."""
    ...


# Allow access to any window property not explicitly defined above.
# This handles dynamically loaded globals like jQuery, lodash, etc.
def __getattr__(name: str) -> Any:
    """Access any window property by name.

    The window object can have arbitrary properties, including:
    - Dynamically loaded libraries (jQuery, lodash, React, etc.)
    - Custom global variables set by JavaScript code
    - Browser-specific APIs not covered by the standard stubs

    Example:
        from anvil.js.window import jQuery as _S
        _S("#my-element").hide()
    """
    ...
