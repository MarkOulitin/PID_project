import styled from "styled-components";

export const GridContainer = styled.div`
  height: 100px;
  width: 1200px;
  background: rgb(248,248,255);
  display: grid;
  grid-gap: 0px 0px;
  grid-template-columns: 1fr 5fr;
`;
export const RowContainer = styled.div`
  text-align: center;
  grid-column-start: 1;
  grid-column-end: span 1;
  border: 1px black solid;
`;
